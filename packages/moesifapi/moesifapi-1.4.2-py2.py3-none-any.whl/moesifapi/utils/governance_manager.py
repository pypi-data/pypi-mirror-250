from governance_util import GovernanceUtil
from moesifapi.exceptions import api_exception

import json

import logging
logger = logging.getLogger(__name__)


class GovernanceRulesManager:
    def __init__(self, api_client):
        self.api_client = api_client
        self.rules = []
        self.user_rules = {}
        self.company_rules = {}
        self.regex_rules = []
        self.unidentified_user_rules = []
        self.unidentified_company_rules = []

    def load_rules(self, DEBUG):
        try:
            get_rules_response = self.api_client.get_governance_rules()
            rules = json.loads(get_rules_response.raw_body)
            self.cache_rules(rules)
            return rules
        except api_exception as inst:
            if 401 <= inst.response_code <= 403:
                print(
                    "[moesif] Unauthorized access getting application configuration. Please check your Application Id.")
            if DEBUG:
                print("[moesif] Error getting governance rules, with status code:", inst.response_code)
            return None
        except Exception as ex:
            if DEBUG:
                print("[moesif] Error getting governance rules:", ex)
            return None

    def cache_rules(self, rules):
        self.rules = rules
        self.user_rules = {}
        self.company_rules = {}
        self.regex_rules = []
        self.unidentified_user_rules = []
        self.unidentified_company_rules = []
        for rule in rules:
            if rule['type'] == 'regex':
                self.regex_rules.append(rule)
            elif rule['type'] == 'user':
                self.user_rules[rule['_id']] = rule
                if rule['applied_to_unidentified']:
                    self.unidentified_user_rules.append(rule)
            elif rule['type'] == 'company':
                self.company_rules[rule['_id']] = rule
                if rule['applied_to_unidentified']:
                    self.unidentified_company_rules.append(rule)

    def has_rules(self):
        return self.rules and len(self.rules) > 0

    def get_applicable_regex_rules(self, request_fields, request_body):
        if self.regex_rules:
            return filter(
                lambda rule: GovernanceUtil.does_regex_config_match(rule['regex_config'], request_fields, request_body),
                self.regex_rules
            )

        return []

    def get_applicable_unidentified_user_rules(self, request_fields, request_body):
        if self.unidentified_user_rules:
            return filter(
                lambda rule: GovernanceUtil.does_regex_config_match(rule['regex_config'], request_fields, request_body),
                self.unidentified_user_rules
            )

        return []

    def get_applicable_unidentified_company_rules(self, request_fields, request_body):
        if self.unidentified_company_rules:
            return filter(
                lambda rule: GovernanceUtil.does_regex_config_match(rule['regex_config'], request_fields, request_body),
                self.unidentified_company_rules
            )

        return []

    def get_user_rules(self, config_rules_values, request_fields, request_body):
        applicable_rules = []
        in_cohort_of_rule_hash = {}

        # if there is entry in config_rules_values it means user is in the cohort of the rule.

        if config_rules_values:
            for rules_values_entry in config_rules_values:
                rule_id = rules_values_entry['rules']
                in_cohort_of_rule_hash[rule_id] = True

                found_rule = self.user_rules[rule_id]
                if not found_rule:
                    # print an debug log here.
                    break

                regex_matched = GovernanceUtil.does_regex_config_match(found_rule['regex_config'], request_fields, request_body)

                if not regex_matched:
                    break

                if found_rule['applied_to'] == 'not_matching':
                    # skipping because apply to user not in cohort
                    break
                else:
                    applicable_rules.append(found_rule)

        # now handle where user is not in cohort.
        for rule in self.user_rules.items():
            rule_info = rule[1]
            if rule_info['applied_to'] == 'not_matching' and not in_cohort_of_rule_hash.get(rule_info['_id'], None):
                regex_matched = GovernanceUtil.does_regex_config_match(rule_info['regex_config'], request_fields, request_body)
                if regex_matched:
                    applicable_rules.append(rule_info)

        return applicable_rules

    def get_company_rules(self, config_rules_values, request_fields, request_body):
        applicable_rules = []
        in_cohort_of_rule_hash = {}

        # if there is entry in config_rules_values it means user is in the cohort of the rule.
        if config_rules_values:
            for rules_values_entry in config_rules_values:
                rule_id = rules_values_entry['rules']
                in_cohort_of_rule_hash[rule_id] = True

                found_rule = self.company_rules[rule_id]
                if not found_rule:
                    # print an debug log here.
                    break

                regex_matched = GovernanceUtil.does_regex_config_match(found_rule['regex_config'], request_fields, request_body)

                if not regex_matched:
                    break

                if found_rule['applied_to'] == 'not_matching':
                    # skipping because apply to user not in cohort
                    break
                else:
                    applicable_rules.append(found_rule)

        # now handle where user is not in cohort.
        for rule in self.company_rules.items():
            rule_info = rule[1]
            if rule_info['applied_to'] == 'not_matching' and not in_cohort_of_rule_hash.get(rule_info['_id'], None):
                regex_matched = GovernanceUtil.does_regex_config_match(rule_info['regex_config'], request_fields, request_body)
                if regex_matched:
                    applicable_rules.append(rule_info)

        return applicable_rules

    def govern_request(self, config, event_info, user_id, company_id, request_body):

        request_fields = GovernanceUtil.prepare_request_fields(event_info, request_body)

        config_json = json.loads(config.raw_body)

        response_holder = {
            'status': None,
            'headers': {},
            'body': None
        }

        applicable_regex_rules = self.get_applicable_regex_rules(request_fields, request_body)

        response_holder = GovernanceUtil.apply_rules(applicable_regex_rules, response_holder, None)

        if company_id is None:
            unidentified_company_rules = self.get_applicable_unidentified_company_rules(request_fields, request_body)
            response_holder = GovernanceUtil.apply_rules(unidentified_company_rules, response_holder, None)
        else:
            config_rules_values = config_json.get('company_rules', {}).get(company_id)
            company_rules = self.get_company_rules(config_rules_values, request_fields, request_body)
            response_holder = GovernanceUtil.apply_rules(company_rules, response_holder, config_rules_values)

        if user_id is None:
            unidentified_user_rules = self.get_applicable_unidentified_user_rules(request_fields, request_body)
            response_holder = GovernanceUtil.apply_rules(unidentified_user_rules, response_holder, None)
        else:
            config_rules_values = config_json.get('user_rules', {}).get(user_id)
            user_rules = self.get_user_rules(config_rules_values, request_fields, request_body)
            response_holder = GovernanceUtil.apply_rules(user_rules, response_holder, config_rules_values)

        if 'blocked_by' in response_holder:
            response_holder['body'] = GovernanceUtil.format_body_for_middleware(response_holder['body'])

        return response_holder
