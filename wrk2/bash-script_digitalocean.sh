# spring  =>  [10001, 60001, 320001, 660001, 3360001, 6380001]
# php  =>  [10001, 110001, 670001, 1320001, 6550001, 12800000]
# django  =>  [10001, 80001, 460001, 950001, 4950001, 9630001]
# golang  =>  [5000, 30001, 210001, 440001, 2900001, 6390001]
# nodejs  =>  [5000, 30001, 140001, 280001, 1850001, 3880001]

#digitaloceanapp

# spring  =>  [20001, 140001, 640001, 1330001, 5670001, 12310001]
# php  =>  [20001, 220001, 1070001, 1950001, 9960001, 17760001]
# django  =>  [10001, 110001, 610001, 1150001, 6340001, 11800001]
# golang  =>  [10001, 100001, 470001, 930001, 4150001, 8000001]
# nodejs  =>  [60001, 840001, 4250001, 9950001, 10110001, 17840001]


# framework_names=("nodejs" "golang" "spring" "django" "php");
# framework_names=("spring" "django" "php");
framework_names=("nodejs");
# urls = ["https://cispa-spring-mwa2y.ondigitalocean.app/" "https://cispa-php-eqct5.ondigitalocean.app/" "https://sample-app-django-ylqr5.ondigitalocean.app/" 
# "https://cispa-golang-3aefj.ondigitalocean.app/" 
# "https://cispa-nodejs-m4lsy.ondigitalocean.app/");

for i in {1..5}; do
    for framework_name in ${framework_names[@]}; do

        if [ "$framework_name" = "nodejs" ]; then
            # payload_number=(60001 840001 4250001 9950001 10110001 17840001) ; #nodejs
            payload_number=(10110001 17840001) ; #nodejs
            url="https://cispa-nodejs-m4lsy.ondigitalocean.app/";
        fi

        if [ "$framework_name" = "golang" ]; then
            payload_number=(10001 100001 470001 930001 4150001 8000001) ; #golang
            url="https://cispa-golang-3aefj.ondigitalocean.app/";  
        fi

        if [ "$framework_name" = "spring" ]; then
            payload_number=(20001 140001 640001 1330001 5670001 12310001) ; #spring
            url="https://cispa-spring-mwa2y.ondigitalocean.app/";
        fi

        if [ "$framework_name" = "django" ]; then
            payload_number=(10001 110001 610001 1150001 6340001 11800001) ; #django
            url="https://sample-app-django-ylqr5.ondigitalocean.app/";
        fi

        if [ "$framework_name" = "php" ]; then
            payload_number=(20001 220001 1070001 1950001 9960001 17760001) ; #php
            url="https://cispa-php-eqct5.ondigitalocean.app/";
        fi
        
        con=1;
        for t in ${payload_number[@]}; do
            request_number=(300 500) ;
            for r in ${request_number[@]}; do
                ./wrk -t1 -c50 -d60s -R$r "$url" $con 50 $framework_name $t 0 $i $r $file_path &
                sleep 10;
                if [ $t = 0 ]; then
                    ./wrk -t1 -c50 -d5s -R2000 "$url?id=${t}" ${con[conn]} 50 $framework_name $t 1 $i $r >> "heroku/${framework_name}_${t}.txt" &
                else
                    ./wrk -t1 -c50 -d5s -R$r "$url?id=${t}" $con 50 $framework_name $t 1 $i $r $file_path &
                fi
                echo "Going to sleep";
                sleep 120;




                ./wrk -t1 -c50 -d60s -R$r $url 1 50 $framework_name $t 0 $i $r &
                sleep 10;
                if [ $t = 0 ]; then
                    ./wrk -t1 -c50 -d5s -R2000 "$url?id=${t}" 1 50 $framework_name $t 1 $i $r >> "digital_ocean_app/${framework_name}_${t}.txt" &
                else
                    ./wrk -t1 -c50 -d5s -R$r "$url?id=${t}" 1 50 $framework_name $t 1 $i $r >> "digital_ocean_app/${framework_name}_${t}_${r}.txt" &
                fi
                echo "Going to sleep";
                sleep 120;
            done
        done
    done
done

# python3 script.py &
# sleep 10;
# python3 malicious.py >> malicious_request_starting_time_with_payload_2.txt;