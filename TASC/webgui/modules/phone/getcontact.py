from Crypto.Cipher import AES
from random import randint
import argparse
import requests
import logging
import hashlib
import base64
import time
import json
import hmac
import sys

codes={'AF': '93', 'AL': '355', 'DZ': '213', 'AS': '1-684', 'AD': '376', 'AO': '244', 'AI': '1-264', 'AQ': '672', 'AG': '1-268', 'AR': '54', 'AM': '374', 'AW': '297', 'AU': '61', 'AT': '43', 'AZ': '994', 'BS': '1-242', 'BH': '973', 'BD': '880', 'BB': '1-246', 'BY': '375', 'BE': '32', 'BZ': '501', 'BJ': '229', 'BM': '1-441', 'BT': '975', 'BO': '591', 'BA': '387', 'BW': '267', 'BR': '55', 'IO': '246', 'VG': '1-284', 'BN': '673', 'BG': '359', 'BF': '226', 'BI': '257', 'KH': '855', 'CM': '237', 'CA': '1', 'CV': '238', 'KY': '1-345', 'CF': '236', 'TD': '235', 'CL': '56', 'CN': '86', 'CX': '61', 'CC': '61', 'CO': '57', 'KM': '269', 'CK': '682', 'CR': '506', 'HR': '385', 'CU': '53', 'CW': '599', 'CY': '357', 'CZ': '420', 'CD': '243', 'DK': '45', 'DJ': '253', 'DM': '1-767', 'DO': '1-809', 'TL': '670', 'EC': '593', 'EG': '20', 'SV': '503', 'GQ': '240', 'ER': '291', 'EE': '372', 'ET': '251', 'FK': '500', 'FO': '298', 'FJ': '679', 'FI': '358', 'FR': '33', 'PF': '689', 'GA': '241', 'GM': '220', 'GE': '995', 'DE': '49', 'GH': '233', 'GI': '350', 'GR': '30', 'GL': '299', 'GD': '1-473', 'GU': '1-671', 'GT': '502', 'GG': '44-1481', 'GN': '224', 'GW': '245', 'GY': '592', 'HT': '509', 'HN': '504', 'HK': '852', 'HU': '36', 'IS': '354', 'IN': '91', 'ID': '62', 'IR': '98', 'IQ': '964', 'IE': '353', 'IM': '44-1624', 'IL': '972', 'IT': '39', 'CI': '225', 'JM': '1-876', 'JP': '81', 'JE': '44-1534', 'JO': '962', 'KZ': '7', 'KE': '254', 'KI': '686', 'XK': '383', 'KW': '965', 'KG': '996', 'LA': '856', 'LV': '371', 'LB': '961', 'LS': '266', 'LR': '231', 'LY': '218', 'LI': '423', 'LT': '370', 'LU': '352', 'MO': '853', 'MK': '389', 'MG': '261', 'MW': '265', 'MY': '60', 'MV': '960', 'ML': '223', 'MT': '356', 'MH': '692', 'MR': '222', 'MU': '230', 'YT': '262', 'MX': '52', 'FM': '691', 'MD': '373', 'MC': '377', 'MN': '976', 'ME': '382', 'MS': '1-664', 'MA': '212', 'MZ': '258', 'MM': '95', 'NA': '264', 'NR': '674', 'NP': '977', 'NL': '31', 'AN': '599', 'NC': '687', 'NZ': '64', 'NI': '505', 'NE': '227', 'NG': '234', 'NU': '683', 'KP': '850', 'MP': '1-670', 'NO': '47', 'OM': '968', 'PK': '92', 'PW': '680', 'PS': '970', 'PA': '507', 'PG': '675', 'PY': '595', 'PE': '51', 'PH': '63', 'PN': '64', 'PL': '48', 'PT': '351', 'PR': '1-787', 'QA': '974', 'CG': '242', 'RE': '262', 'RO': '40', 'RU': '7', 'RW': '250', 'BL': '590', 'SH': '290', 'KN': '1-869', 'LC': '1-758', 'MF': '590', 'PM': '508', 'VC': '1-784', 'WS': '685', 'SM': '378', 'ST': '239', 'SA': '966', 'SN': '221', 'RS': '381', 'SC': '248', 'SL': '232', 'SG': '65', 'SX': '1-721', 'SK': '421', 'SI': '386', 'SB': '677', 'SO': '252', 'ZA': '27', 'KR': '82', 'SS': '211', 'ES': '34', 'LK': '94', 'SD': '249', 'SR': '597', 'SJ': '47', 'SZ': '268', 'SE': '46', 'CH': '41', 'SY': '963', 'TW': '886', 'TJ': '992', 'TZ': '255', 'TH': '66', 'TG': '228', 'TK': '690', 'TO': '676', 'TT': '1-868', 'TN': '216', 'TR': '90', 'TM': '993', 'TC': '1-649', 'TV': '688', 'VI': '1-340', 'UG': '256', 'UA': '380', 'AE': '971', 'GB': '44', 'US': '1', 'UY': '598', 'UZ': '998', 'VU': '678', 'VA': '379', 'VE': '58', 'VN': '84', 'WF': '681', 'EH': '212', 'YE': '967', 'ZM': '260', 'ZW': '263'}
country_code=""
# Global vars
HMAC_key = "2Wq7)qkX~cp7)H|n_tc&o+:G_USN3/-uIi~>M+c ;Oq]E{t9)RC_5|lhAA_Qq%_4"
AES_key = bytes.fromhex("{}".format("a352a81da6488fbf08fdcbadd60b5a2b7a0cae468cf9766125b5806d92e10da5"))
token="AxPu296ea819925d2998e593e46c0cdc342e1d30c2d80921dc7f375497f3"
device_id = "27b6dc0c3cb{}".format(randint(10000, 90000))
exp = int("2627976")
mod = 900719925481

# Others
base_url = "https://pbssrv-centralevents.com"
base_uri_api = "/v2.1/"
methods = {"number-detail": "details", "search": "search", "verify-code": "", "register": ""}
timestamp = str(time.time()).split(".")[0]


env_data = [{"token": "krtULaf8fe19927fa8a1e2d28c995578a7c16a76c721f584661d0b63751",
			 "aes_key": "0d7f40a508d2d8a2437b17f94d6fb7d22296426ea954038266718c703e58146a",
			 "name": "chipik"},
			{"token": "hxgIn27234563018a7ba312b501c39b0f2f8816ee9c1a4d7ed30f9d3369",
			 "aes_key": "7499b9c9a0ff9028c6bff50835857db120d7bb8cf8ba3d0b5ec3e65193622ac9",
			 "name": "vika"},
			{"token":"kFktvae5f375e7454d6da16bd263c88114f8702eb21692988f7035c3908",
			 "aes_key":"e7bb64e60cbb9644bdbd34b1c72aaf424619d0a26ec3d25aebba01389351800a",
			 "name":"4ekin"}
			]

headers = {
	"X-App-Version": "4.2.0",
	"X-Req-Timestamp": timestamp,
	"X-Os": "android 7.1.1",
	"X-Token": token,
	"X-Encrypted": "1",
	"X-Client-Device-Id": device_id,
	"X-Req-Signature": "",
	"Content-Type": "application/json; charset=utf-8",
	"Connection": "close",
	"Accept-Encoding": "gzip, deflate"}

data = {"countryCode": country_code,
		"phoneNumber": "919486324742",
		"source": "",
		"token": token,
		}

captcha_data = {"token": token,
				"validationCode": "",
				}

new_vars_data = {"adjustId": "aa8a3ea2e1c10552070e3aeb93d0cfea",
				 "adjustParams":
					 {"adid": "aa8a3ea2e1c10552070e3aeb93d0cfea",
					  "network": "Organic",
					  "trackerName": "Organic",
					  "trackerToken": "5nd8yt7"
					  },
				 "androidId": device_id,
				 "countryCode": country_code,
				 "deviceName": "Android~SDK~built~for~x86",
				 "deviceType": "Android",
				 "gpsAdid": "273c9507-1d80-4913-b3f0-03e5fde34810",
				 "peerKey": "734470887651",
				 "timeZone": "Europe/Moscow"
				 }


def set_new_token(new_token):
	global token
	token = new_token
	headers["X-Token"] = token
	data["token"] = token
	captcha_data["token"] = token


def set_new_aes_key(new_aes_key):
	global AES_key
	# AES_key = "{}".format(new_aes_key).decode("hex")
	AES_key = bytes.fromhex("{}".format(new_aes_key))


def set_new_exp(new_exp):
	global exp
	exp = int(new_exp)


def set_new_device_id(new_device_id):
	global device_id
	headers["X-Client-Device-Id"] = new_device_id
	new_vars_data["androidId"] = new_device_id
	device_id = new_device_id


def calculate_new_aes_key(serverKey):
	print("Calculating new AES key. It can takes time...")
	longInt = int(serverKey) ** exp % mod
	new_key = hashlib.sha256(bytearray(str(longInt), "utf-8")).hexdigest()
	return str(new_key)


def get_new_vars():
	print("Getting new token and AES key...")
	method = "register"
	headers["X-Token"] = ""
	result = send_req_to_the_server(base_url + base_uri_api + method, new_vars_data, True)
	new_token = result["result"]["token"]
	serverKey = result["result"]["serverKey"]
	# serverKey = 408701071142
	print("Params:\n" \
		  "token: {}\n" \
		  "serverkey: {}\n" \
		  "exp: {}\n" \
		  "mod: {}".format(new_token, serverKey, exp, mod))
	new_key = calculate_new_aes_key(serverKey)
	print("New token: {}\nNew AES key:{}".format(new_token, new_key))
	set_new_token(token)
	set_new_aes_key(new_key)


def set_random_env():
	if len(env_data):
		rand = randint(0, len(env_data) - 1)
		token = env_data[rand]["token"]
		aes_key = env_data[rand]["aes_key"]
		set_new_token(token)
		set_new_aes_key(aes_key)


def get_vars():
	return (AES_key.encode("hex"), token, device_id, exp)


def prepare_payload(payload):
	return json.dumps(payload).replace(" ", "").replace("~", " ")


def create_sign(timestamp, payload):
	message = bytes("{}-{}".format(timestamp, payload), encoding="utf8")
	secret = bytes(HMAC_key, encoding="utf8")
	signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
	return signature


def send_post(url, data):
	r = requests.post(url, data=data, headers=headers)
	if r.status_code == 200:
		return r.json()["data"]
	if r.status_code == 201:
		return r.json()
	elif r.status_code == 404:
		print("Nothing found for {} :(".format("919486324742"))
	elif r.status_code == 403:
		return r.json()["data"]
	elif r.status_code == 400:
		print("Wrong Number? Status: {}".format(r.status_code))
		return r.json()["data"]
	else:
		print("Something wrong! Status: {}".format(r.status_code))
	return r.status_code


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]


def decrypt_aes(payload):
	cipher = AES.new(AES_key, AES.MODE_ECB)
	rez = unpad(str(cipher.decrypt(payload),"utf-8"))
	return rez


def encrypt_aes(strr):
	raw = pad(strr)
	cipher = AES.new(AES_key, AES.MODE_ECB)
	return str(base64.b64encode(cipher.encrypt(raw)), "utf-8")


def send_req_to_the_server(url, payload, no_encrypt=False):
	headers["X-Req-Signature"] = create_sign(timestamp, prepare_payload(payload))
	if no_encrypt:
		headers["X-Encrypted"] = "0"
		result_dec = send_post(url, prepare_payload(payload))
		return result_dec
	else:
		result_enc = send_post(url, json.dumps({"data": encrypt_aes(prepare_payload(payload))}))
	if isinstance(result_enc, int):
		result = {"meta": {}}
		result["meta"]["httpStatusCode"] = result_enc
		result["meta"]["errorCode"] = result_enc
		result["meta"]["errorMessage"] = str(result_enc)
		return result
	else:
		return json.loads(decrypt_aes(base64.b64decode(result_enc)))


def print_results(profile, remainingCount):
    return (profile)

def handle_captcha(imgstring):
	imgdata = base64.b64decode(imgstring)
	filename = "captcha_{}.jpg".format(randint(0, 1000))
	with open(filename, "wb") as f:
		f.write(imgdata)
	print("Captcha saved in file: {}".format(filename))
	print("[!] Check it and type it below. ")
	captcha_value = input("Enter captcha:")
	method = "verify-code"
	captcha_data["validationCode"] = captcha_value
	result = send_req_to_the_server(base_url + base_uri_api + method, captcha_data)
	if result["meta"]["httpStatusCode"] == 200:
		print("Captcha passed. Now you can try search again!")
		return 0
	elif result["meta"]["httpStatusCode"] == 403:
		code = result["meta"]["errorCode"]
		print("Error ({}):".format(code)),
		print(result["meta"]["errorMessage"])
		if code == "403004":
			print("Wrong Captcha!")
	return 1


def save_captcha_bot(imgstring):
	imgdata = base64.b64decode(imgstring)
	filename = "captcha/captcha_{}.jpg".format(randint(0, 1000))
	with open(filename, "wb") as f:
		f.write(imgdata)
	print("Captcha saved in file: {}".format(filename))
	return filename


def send_captcha_bot(captcha_value):
	method = "verify-code"
	captcha_data["validationCode"] = captcha_value
	result = send_req_to_the_server(base_url + base_uri_api + method, captcha_data)
	if result["meta"]["httpStatusCode"] == 200:
		print("Captcha passed. Now you can try search again!")
		return 0
	elif result["meta"]["httpStatusCode"] == 403:
		code = result["meta"]["errorCode"]
		print("Error ({}):".format(code), )
		print(result["meta"]["errorMessage"])
		if code == "403004":
			print("Wrong Captcha!")
	return 1

def get_acc_name_by_token(token_val):
	for env in env_data:
		if env["token"] == token_val:
			return env["name"]
	return ""

def get_number_info(phoneNumber):
	global country_code
	phone=phoneNumber.replace("+","")
	for i in codes.keys():
		if phone[:len(codes[i])] == codes[i]:
			country_code=i
			break
	method = "search"
	data["source"] = methods[method]
	data["phoneNumber"] = phoneNumber
	set_random_env()
	result = send_req_to_the_server(base_url + base_uri_api + method, data)
	if result["meta"]["httpStatusCode"] == 200:
		profile = result["result"]["profile"]
		profile["tags"] = []
		remainingCount = result["result"]["subscriptionInfo"]["usage"]["search"]["remainingCount"]
	elif result["meta"]["httpStatusCode"] == 403:
		code = result["meta"]["errorCode"]
		print("Error ({}):".format(code)),
		print(result["meta"]["errorMessage"])
		img_file = ""
		if code == "403004":
			img_file = save_captcha_bot(result["result"]["image"])
		return [result["meta"]["httpStatusCode"], [code, img_file]]
	elif result["meta"]["httpStatusCode"] == 400:
		code = result["meta"]["errorCode"]
		print("Error ({}):".format(code)),
		print(result["meta"]["errorMessage"])
		return [result["meta"]["httpStatusCode"], ""]
	elif result["meta"]["httpStatusCode"] == 404:
		code = result["meta"]["errorCode"]
		print("Error ({}):".format(code)),
		print(result["meta"]["errorMessage"])
		return [result["meta"]["httpStatusCode"], ""]
	else:
		print("Something wrong!")
		return [777, ""]
		# return 0
	if profile["tagCount"] > 0:
		# 1 - /v2.1/number-detail
		method = "number-detail"
		data["source"] = methods[method]
		headers["X-Req-Signature"] = create_sign(timestamp, prepare_payload(data))
		result_enc = send_post(base_url + base_uri_api + method,
							   json.dumps({"data": encrypt_aes(prepare_payload(data))}))
		result_dec = json.loads(decrypt_aes(base64.b64decode(result_enc)))
		if result_dec["meta"]["httpStatusCode"] == 200:
			tags_nbr = len(result_dec["result"]["tags"])
			remainingCount = result["result"]["subscriptionInfo"]["usage"]["search"]["remainingCount"]
			for tag in result_dec["result"]["tags"]:
				profile["tags"].append(tag["tag"])
	#print_results(profile, remainingCount)
	return profile
def getcontact(Phonenumber):
	while 1:
		try:
			data = get_number_info(Phonenumber)
			print(data)
			if "Error" in data:
				continue
			else:
				return data
		except:
			pass

#getcontact("+917010951718")