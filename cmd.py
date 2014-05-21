USERNAME="admin"
PASSWORD="default"
CSRF_ENABLED=True
SECERT_KEY="a session key"
LOGFILE="/var/log/nginx/access.log.1"
#cmd result need follow type:
# class number
# example:
# 192.168.0.1 24
# the up line represent 192.168.0.1 access page 24 
CMD1="cat "+LOGFILE+"|awk -F\" \" '{A[$1]++}; END{for(i in A)print i,A[i]}'|sort -r -k2"
#have five Graph Type 
# 1 Line char
# 2 pie char
# 3 Colum char
# 4 Bar char
GRAPHTYPE1=2
TITLE1="Access Page number"
CMD2="cat "+LOGFILE+"|awk -F\" \" '{A[substr($NF,1,length($NF)-1)]++}END{for(i in A)print i,A[i]}'|sort -r -k2"
GRAPHTYPE2=3
TITLE2="Brower type and number"
