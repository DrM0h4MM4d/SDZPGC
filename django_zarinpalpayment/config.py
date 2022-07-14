from django.conf import settings



class ZarinPalConfig:
    def __init__(self):

        payment = getattr(settings, 'ZARINPAL', None)
        
        self.merchant_id = payment['merchant_id']
        self.payment_check = payment['is_sandbox']
        self.payment_callback = payment['callback_url']


        if self.payment_check:
            self.payment_request = payment['sandbox']['request']
            self.payment_verify = payment['sandbox']['verify']
            self.payment_startpay = payment['sandbox']['startpay']
        else:
            self.payment_request = payment['default']['request']
            self.payment_verify = payment['default']['verify']
            self.payment_startpay = payment['default']['startpay']


    def get_request_results(self, dict_result):
        authority = dict_result['data']['authority']
        
        if not dict_result.get('errors'):
            return self.payment_startpay.format(authority=authority)
        else:
            e_code = dict_result['errors']['code']
            e_message = dict_result['errors']['message']
            return {"error": {"message": e_message, "code": e_code}}


    def get_verify_results(self, dict_result):
        if len(dict_result['errors']) == 0:
            t_status = dict_result['data']['code']
            if t_status == 100:
                return dict_result['data']['ref_id']
            
            elif t_status == 101:
                return dict_result['data']['message']
            
            else:
                return dict_result['data']['message']
        
        else:
            e_code = dict_result['errors']['code']
            e_message = dict_result['errors']['message']
            return {"error": {"message": e_message, "code": e_code}}


    def get_request_data(self, amount, description, mobile=None, email=None):
        req_data = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "callback_url": self.payment_callback,
            "description": description,
            # "metadata": {"mobile": mobile, "email": email}
        }
        return req_data


    def get_verify_data(self, amount, t_authority):
        req_data = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": t_authority
        }
        return req_data

    def get_headers(self):
        req_header = {"accept": "application/json",
            "content-type": "application/json'"}
        return req_header


zconfig = ZarinPalConfig()