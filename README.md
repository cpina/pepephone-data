# pepephone-data
Quick way to check usage data of pepephone (can be used from command line or cgi)

Create a file in one of the places:
$HOME/.pepephone
/etc/pepephone

With this contents:
```
[authentication]
email = email_used_to_authenticate_on_pepephone.com
password = password_for_your_pepephone_account
phone = your_pepephone_phone_number
```

Execute show-data-used.py (or from a CGI it will print the header).

Example output:
```
Getting authorization code...
Getting consumption...

GB total    : 23.00 GB
GB used     : 1.81 GB
GB remaining: 21.19 GB

% Used      : 7.85%
% Month     : 13.33%
```
