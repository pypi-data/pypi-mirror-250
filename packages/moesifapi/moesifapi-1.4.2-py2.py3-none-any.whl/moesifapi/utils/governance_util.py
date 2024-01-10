import json
import re
from functools import reduce

import logging
logger = logging.getLogger(__name__)


class GovernanceUtil(object):

    @staticmethod
    def get_field_value_for_path(cls, path, request_fields={}, request_body={}):
        if path and path.startswith('request.body.') and request_body and isinstance(request_body, dict):
            return request_body.get(path.replace('request.body.', ''), None)
        return request_fields.get(path, None)

    @staticmethod
    def does_regex_config_match(cls, regex_config, request_fields, request_body):
        if not regex_config:
            return True

        def does_one_condition_match(condition):
            path = condition['path']
            field_value = GovernanceUtil.get_field_value_for_path(path, request_fields, request_body)
            regex_pattern = condition['value']
            if field_value:
                return re.search(regex_pattern, field_value)
            else:
                return False

        def does_one_set_of_conditions_match(one_regex_config):
            conditions = one_regex_config['conditions']
            if not conditions:
                return False
            values_to_and = map(does_one_condition_match, conditions)
            return reduce(lambda x, y: x and y, values_to_and, True)

        values_to_or = map(does_one_set_of_conditions_match, regex_config)
        return reduce(lambda x, y: x or y, values_to_or, False)

    @staticmethod
    def recursively_replace_values(cls, temp_val, merge_tag_values={}, rule_variables=None):
        if not rule_variables:
            return temp_val

        if not temp_val:
            return temp_val

        if isinstance(temp_val, str):
            result = temp_val
            for rule_variable in rule_variables:
                name = rule_variable['name']
                value = merge_tag_values.get(name, 'UNKNOWN')
                result = result.replace('{{' + name + '}}', value)
            return result

        if type(temp_val) is dict:
            result = {}
            for key in temp_val:
                result[key] = GovernanceUtil.recursively_replace_values(temp_val[key], merge_tag_values, rule_variables)
            return result

        if type(temp_val) is list:
            return map(lambda x: GovernanceUtil.recursively_replace_values(x, merge_tag_values, rule_variables), temp_val)

        # for all other types just return value
        return temp_val

    @staticmethod
    def modify_response_for_one_rule(cls, response_holder, rule, merge_tag_values):
        rule_variables = {}
        if 'variables' in rule:
            rule_variables = rule['variables']

        if 'response' in rule and 'headers' in rule['response']:
            rule_headers = rule['response']['headers']
            if rule_headers:
                value_replaced_headers = GovernanceUtil.recursively_replace_values(rule_headers, merge_tag_values, rule_variables)
                for header_key in value_replaced_headers:
                    response_holder['headers'][header_key] = value_replaced_headers[header_key]

        if 'block' in rule and rule['block']:
            response_holder['blocked_by'] = rule['_id']
            rule_res_body = rule['response']['body']
            response_holder['body'] = GovernanceUtil.recursively_replace_values(rule_res_body, merge_tag_values, rule_variables)
            response_holder['status'] = rule['response']['status']

        return response_holder

    @staticmethod
    def apply_one_rule(cls, response_holder, rule, config_rule_values):
        merge_tag_values = {}
        if config_rule_values:
            for one_entry in config_rule_values:
                if one_entry['rules'] == rule['_id']:
                    if 'values' in one_entry:
                        merge_tag_values = one_entry['values']

        return GovernanceUtil.modify_response_for_one_rule(response_holder, rule, merge_tag_values)

    @staticmethod
    def apply_rules(cls, applicable_rules, response_holder, config_rules_values):
        try:
            if not applicable_rules:
                return response_holder

            for rule in applicable_rules:
                response_holder = GovernanceUtil.apply_one_rule(response_holder, rule, config_rules_values)

            return response_holder
        except Exception as ex:
            logger.debug('failed to apply rules ' + str(ex))
            return response_holder

    @staticmethod
    def format_body_for_middleware(cls, body):
        return [json.dumps(body).encode('utf-8')]

    @staticmethod
    def prepare_request_fields(cls, event_info, request_body):
        fields = {
            'request.verb': event_info.method,
            'request.ip': event_info.ip_address,
            'request.route': event_info.url,
            'request.body.operationName': request_body.get('operationName', None) if request_body and isinstance(
                request_body, dict) else None
        }

        return fields
