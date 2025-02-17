import re

text = '<optionid="az_sn">SF17662</option><optionid="az_sn">AZ68005431</option><optionid="az_sn">AZ93851590</option>'

pattern = 'SF\d+'
matches = re.finditer(pattern, text)
for match in matches:
    print(match.group())  # 输出匹配到的内容

aa = {'code': 0, 'error': '', 'msg': 'success',
      'data': {'reviewed': True, 'isZero': False, 'useBt3Ds': True, 'needOrderDetail': True, 'creditPay': True,
               'summary': {'totalAmount': '5.47', 'orderAccountBalanceAmount': '0', 'totalAmountExchange': '5.47',
                           'shippingFee': '0', 'shippingFeeExchange': '0', 'goodsAmount': 0,
                           'goodsAmountExchange': '10', 'bonus': 5, 'referralDiscount': 0, 'bonusExchange': 5,
                           'shippingFeeDisplay': '$0', 'shippingFeeExchangeDisplay': '$0', 'goodsAmountDisplay': '$0',
                           'goodsAmountExchangeDisplay': '$10', 'bonusDisplay': '$5', 'referralDiscountDisplay': '$0',
                           'bonusExchangeDisplay': '$5', 'referralDiscountExchangeDisplay': '$0',
                           'totalAmountExchangeDisplay': '$5.47', 'totalAmountDisplay': '$5.47',
                           'orderAccountBalanceAmountDisplay': '$0', 'editable': True, 'lastGetTime': '0000-00-00',
                           'originalShippingFee': '', 'rushFee': '0', 'rushFeeDisplay': '$0', 'totalRushFee': 0,
                           'totalRushFeeDisplay': '$0', 'taxRatio': '', 'originTaxFee': 0.47,
                           'originTaxFeeDisplay': '$0.47', 'taxFee': '0.47', 'taxFeeDisplay': '$0.47',
                           'NYStateRate': '', 'NYRateDuty': 0, 'NYRateDutyDisplay': '$0', 'rebateTaxFee': None,
                           'rebateTaxFeeDisplay': None, 'rebateTaxRatio': None, 'totalNoDealGoodsAmount': 0,
                           'totalNoDealGoodsAmountDisplay': '$0', 'goodsQty': 1, 'canUseInstallmentsPlan': False,
                           'canUseTicket': False, 'hasAfterPay': True, 'hasKlarna': True, 'canUseAfterPay': False,
                           'afterPayTips': 'Afterpay available for orders $49 -$2000 (excluding At-Home Try On dresses)',
                           'cashAppPayTips': 'Cash App Pay available for orders $49 -$2000 (excluding At-Home Try On dresses)',
                           'canUseKlarna': False,
                           'klarnaTips': 'Klarna available for orders $49 - $2,000 (excluding At-Home Try On dresses)'},
               'addressInfo': {'shippingAddress': {'addressId': 3589174, 'addressType': 'SHIPPING', 'addressName': '',
                                                   'userId': 5872495, 'consignee': 'yong shi', 'firstName': 'yong',
                                                   'lastName': 'shi', 'gender': '', 'email': 'shiyong@gaoyaya.com',
                                                   'country': 3859, 'province': 3871, 'provinceText': 'California',
                                                   'city': 385920049360, 'district': 0, 'address': 'cccccccccccc',
                                                   'zipcode': '95112', 'tel': '1555541155', 'mobile': '',
                                                   'signBuilding': '', 'bestTime': '', 'cityText': 'San Jose',
                                                   'districtText': '', 'isDefault': 1, 'taxCodeType': 0,
                                                   'taxCodeValue': '', 'doorplate': '', 'taxNumber': '', 'parentId': 0,
                                                   'countryName': 'United States', 'provinceName': 'California',
                                                   'cityName': None, 'countryCode': 'US', 'provinceCode': 'CA',
                                                   'fullName': 'yong shi', 'fullAddress': 'cccccccccccc'},
                               'billingAddress': {'addressId': 3589163, 'addressType': 'BILLING', 'addressName': '',
                                                  'userId': 5872495, 'consignee': 'yong shi', 'firstName': 'yong',
                                                  'lastName': 'shi', 'gender': '', 'email': '', 'country': 3859,
                                                  'province': 3871, 'provinceText': 'California', 'city': 385920049360,
                                                  'district': 0, 'address': 'ccccccccccccc', 'zipcode': '95112',
                                                  'tel': '1211211252', 'mobile': '', 'signBuilding': '', 'bestTime': '',
                                                  'cityText': 'San Jose', 'districtText': '', 'isDefault': 0,
                                                  'taxCodeType': 0, 'taxCodeValue': '', 'doorplate': '',
                                                  'taxNumber': '', 'parentId': 0, 'countryName': 'United States',
                                                  'provinceName': 'California', 'cityName': None, 'countryCode': 'US',
                                                  'provinceCode': 'CA', 'fullName': 'yong shi',
                                                  'fullAddress': 'ccccccccccccc'}, 'pickUpAddress': []},
               'paymentInfo': {'paymentId': 186, 'name': 'Credit/Debit Card', 'code': 'braintree',
                               'token': 'eyJ2ZXJzaW9uIjoyLCJhdXRob3JpemF0aW9uRmluZ2VycHJpbnQiOiJleUowZVhBaU9pSktWMVFpTENKaGJHY2lPaUpGVXpJMU5pSXNJbXRwWkNJNklqSXdNVGd3TkRJMk1UWXRjMkZ1WkdKdmVDSXNJbWx6Y3lJNkltaDBkSEJ6T2k4dllYQnBMbk5oYm1SaWIzZ3VZbkpoYVc1MGNtVmxaMkYwWlhkaGVTNWpiMjBpZlEuZXlKbGVIQWlPakUzTXpZeU16Z3dORE1zSW1wMGFTSTZJbU0xWVRnMVpHTTVMVE16WkRZdE5EVTVOUzFoTWpsakxXTTJOV1V5WmpkaE4yUTVaU0lzSW5OMVlpSTZJbTV5YzJSemEzRTVOMjQyYm1zelpETWlMQ0pwYzNNaU9pSm9kSFJ3Y3pvdkwyRndhUzV6WVc1a1ltOTRMbUp5WVdsdWRISmxaV2RoZEdWM1lYa3VZMjl0SWl3aWJXVnlZMmhoYm5RaU9uc2ljSFZpYkdsalgybGtJam9pYm5KelpITnJjVGszYmpadWF6TmtNeUlzSW5abGNtbG1lVjlqWVhKa1gySjVYMlJsWm1GMWJIUWlPbVpoYkhObGZTd2ljbWxuYUhSeklqcGJJbTFoYm1GblpWOTJZWFZzZENKZExDSnpZMjl3WlNJNld5SkNjbUZwYm5SeVpXVTZWbUYxYkhRaVhTd2liM0IwYVc5dWN5STZlMzE5LmJkaWwtNjZ1TGN1MFgzLWE0LVVpSlNmSVo3X3YxRmRSNG5ZVTFQYk9ZWk5QOE5VTGtNRE40c3hSc2MxMEZqSXlJM1E3cjktUkxCamt4VDdqTzZndklnIiwiY29uZmlnVXJsIjoiaHR0cHM6Ly9hcGkuc2FuZGJveC5icmFpbnRyZWVnYXRld2F5LmNvbTo0NDMvbWVyY2hhbnRzL25yc2Rza3E5N242bmszZDMvY2xpZW50X2FwaS92MS9jb25maWd1cmF0aW9uIiwiZ3JhcGhRTCI6eyJ1cmwiOiJodHRwczovL3BheW1lbnRzLnNhbmRib3guYnJhaW50cmVlLWFwaS5jb20vZ3JhcGhxbCIsImRhdGUiOiIyMDE4LTA1LTA4IiwiZmVhdHVyZXMiOlsidG9rZW5pemVfY3JlZGl0X2NhcmRzIl19LCJjbGllbnRBcGlVcmwiOiJodHRwczovL2FwaS5zYW5kYm94LmJyYWludHJlZWdhdGV3YXkuY29tOjQ0My9tZXJjaGFudHMvbnJzZHNrcTk3bjZuazNkMy9jbGllbnRfYXBpIiwiZW52aXJvbm1lbnQiOiJzYW5kYm94IiwibWVyY2hhbnRJZCI6Im5yc2Rza3E5N242bmszZDMiLCJhc3NldHNVcmwiOiJodHRwczovL2Fzc2V0cy5icmFpbnRyZWVnYXRld2F5LmNvbSIsImF1dGhVcmwiOiJodHRwczovL2F1dGgudmVubW8uc2FuZGJveC5icmFpbnRyZWVnYXRld2F5LmNvbSIsInZlbm1vIjoib2ZmIiwiY2hhbGxlbmdlcyI6W10sInRocmVlRFNlY3VyZUVuYWJsZWQiOnRydWUsImFuYWx5dGljcyI6eyJ1cmwiOiJodHRwczovL29yaWdpbi1hbmFseXRpY3Mtc2FuZC5zYW5kYm94LmJyYWludHJlZS1hcGkuY29tL25yc2Rza3E5N242bmszZDMifSwiYXBwbGVQYXkiOnsiY291bnRyeUNvZGUiOiJVUyIsImN1cnJlbmN5Q29kZSI6IlVTRCIsIm1lcmNoYW50SWRlbnRpZmllciI6Im1lcmNoYW50LmNvbS5hemF6aWUuaW9zIiwic3RhdHVzIjoibW9jayIsInN1cHBvcnRlZE5ldHdvcmtzIjpbInZpc2EiLCJtYXN0ZXJjYXJkIiwiYW1leCIsImRpc2NvdmVyIl19LCJwYXlwYWxFbmFibGVkIjp0cnVlLCJwYXlwYWwiOnsiYmlsbGluZ0FncmVlbWVudHNFbmFibGVkIjp0cnVlLCJlbnZpcm9ubWVudE5vTmV0d29yayI6ZmFsc2UsInVudmV0dGVkTWVyY2hhbnQiOmZhbHNlLCJhbGxvd0h0dHAiOnRydWUsImRpc3BsYXlOYW1lIjoiZ2FveWF5YSIsImNsaWVudElkIjoiQVhLWEx1T3ZOblVnbldkejFISHo2ODRwMklmazh2eHQwcmw4Ml9qZlgzUVRBeE5iYWRLTVRrOF9jZWNrOHBUZWVWc19yWFA0ZnJmSnpyTkciLCJiYXNlVXJsIjoiaHR0cHM6Ly9hc3NldHMuYnJhaW50cmVlZ2F0ZXdheS5jb20iLCJhc3NldHNVcmwiOiJodHRwczovL2NoZWNrb3V0LnBheXBhbC5jb20iLCJkaXJlY3RCYXNlVXJsIjpudWxsLCJlbnZpcm9ubWVudCI6Im9mZmxpbmUiLCJicmFpbnRyZWVDbGllbnRJZCI6Im1hc3RlcmNsaWVudDMiLCJtZXJjaGFudEFjY291bnRJZCI6InVzZCIsImN1cnJlbmN5SXNvQ29kZSI6IlVTRCJ9fQ==',
                               'useBt3Ds': True,
                               'billingAddress': {'addressId': 3589163, 'addressType': 'BILLING', 'addressName': '',
                                                  'userId': 5872495, 'consignee': 'yong shi', 'firstName': 'yong',
                                                  'lastName': 'shi', 'gender': '', 'email': '', 'country': 3859,
                                                  'province': 3871, 'provinceText': 'California', 'city': 385920049360,
                                                  'district': 0, 'address': 'ccccccccccccc', 'zipcode': '95112',
                                                  'tel': '1211211252', 'mobile': '', 'signBuilding': '', 'bestTime': '',
                                                  'cityText': 'San Jose', 'districtText': '', 'isDefault': 0,
                                                  'taxCodeType': 0, 'taxCodeValue': '', 'doorplate': '',
                                                  'taxNumber': '', 'parentId': 0, 'countryName': 'United States',
                                                  'provinceName': 'California', 'cityName': None, 'countryCode': 'US',
                                                  'provinceCode': 'CA', 'fullName': 'yong shi',
                                                  'fullAddress': 'ccccccccccccc'}, 'usePaymentGateWay': False,
                               'REF': '10111010', 'useBraintree': True, 'cardNumber': '4000000000001000',
                               'last4CardNumber': '1000'},
               'orderInfo': {'orderId': '', 'orderSn': 'ZZ7197338157', 'userId': 5872495,
                             'orderTime': '2025-01-06 00:20:42', 'payTime': '0000-00-00 00:00:00', 'languageId': 1,
                             'orderStatus': 0, 'shippingStatus': 0, 'payStatus': 0, 'consignee': 'yong shi',
                             'gender': '', 'email': 'shiyong@gaoyaya.com', 'country': 3859, 'province': 3871,
                             'provinceText': 'California', 'city': 385920049360, 'cityText': 'San Jose', 'district': 0,
                             'districtText': '', 'address': 'cccccccccccc', 'zipcode': '95112', 'tel': '1555541155',
                             'mobile': '', 'signBuilding': '', 'bestTime': '', 'shippingId': 91, 'smId': 2,
                             'shippingFee': 0, 'shippingFeeExchange': 0, 'shippingFeeExchangeDisplay': 0,
                             'paymentId': 186, 'paymentFee': '0', 'paymentName': 'Credit/Debit Card',
                             'orderAmount': 5.47, 'orderAmountExchange': 5.47, 'orderAmountExchangeDisplay': 5.47,
                             'goodsAmount': 10, 'goodsAmountExchange': 10, 'goodsAmountExchangeDisplay': 10,
                             'bonus': -5, 'bonusExchange': -5, 'baseCurrencyId': 1, 'orderCurrencyId': 1,
                             'orderCurrencySymbol': 'US$', 'displayCurrencyId': 1, 'rate': '100.0000/100.0000',
                             'displayCurrencyRate': '', 'couponCode': 'forever111', 'projectName': 'azazie',
                             'fromDomain': 'ft1.azazie.com', 'userAgentId': 'python-requests/2.31.0', 'postscript': '',
                             'importantDay': '0000-00-00', 'shippingDateEstimate': '0000-00-00',
                             'gaTrackId': 'a49d079587f1f1335920eae127044404', 'trackId': '', 'taxFee': 0.47,
                             'taxFeeExchange': 0.47, 'taxFeeExchangeDisplay': 0.47, 'activityCouponCode': '',
                             'currency': 'USD', 'display_currency_rate': '100.0000/100.0000', 'doorplate': '',
                             'taxNumber': '', 'shippingType': 1, 'orderAccountBalanceAmount': 0, 'goodsBonus': -5,
                             'shippingBonus': 0, 'rushFee': 0, 'referralDiscount': 0, 'goodsWithoutRushFeeAmount': 0,
                             'rushBonus': 0, 'orderAccountBalanceAmountExchange': 0,
                             'orderAccountBalanceAmountExchangeDisplay': 0, 'orderAccountBalanceAmountDisplay': 0,
                             'orderAmountDisplay': 5.47, 'goodsAmountDisplay': 10, 'bonusExchangeDisplay': -5,
                             'bonusDisplay': -5, 'goodsBonusExchange': -5, 'goodsBonusExchangeDisplay': -5,
                             'goodsBonusDisplay': -5, 'shippingBonusExchange': 0, 'shippingBonusExchangeDisplay': 0,
                             'shippingBonusDisplay': 0, 'shippingFeeDisplay': 0, 'taxFeeDisplay': 0.47,
                             'rushFeeExchange': 0, 'rushFeeExchangeDisplay': 0, 'rushFeeDisplay': 0,
                             'referralDiscountExchange': 0, 'referralDiscountExchangeDisplay': 0,
                             'referralDiscountDisplay': 0, 'goodsWithoutRushFeeAmountExchange': 0,
                             'goodsWithoutRushFeeAmountExchangeDisplay': 0, 'goodsWithoutRushFeeAmountDisplay': 0,
                             'rushBonusExchange': 0, 'rushBonusExchangeDisplay': 0, 'rushBonusDisplay': 0,
                             'countryCode': 'US'}, 'countryCode': 'US', 'currencyCode': 'USD'}}
