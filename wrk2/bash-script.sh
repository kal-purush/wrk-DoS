# payload_number=(1 100 1000 5000 10000 25000 50000 100000 250000 500000 1000000) ; #php
# payload_number=(1 10 50 100 1000 1500 3000 4000 5000 10000 20000 30000 40000 50000) ; #spring, golang

# payload_number=(1 10 50 100 1000 1500 3000 4000 5000 10000 50000) ; 

# payload_number=(1 10 50 100 500 1000 1500 2000 2500 3000 3500 4000 5000);



# payload_number=(501 2001 5001 7001 16001 23001) ; #nodejs
# payload_number=(101 201 601 801 1701 2501) ; #django
# payload_number=(1001 4001 9001 13001 29001 41001) ; #spring
# payload_number=(10001 70001 390001 750001 3770001 7680001) ; #php 
# payload_number=(2001 5001 12001 18001 39001 55001) ; #golang

#for regex

# payload_number=(15 18 21 22 24 25) ; #nodejs
# payload_number=(10001 90001 410001 850001 4190001 8510001) ; #django
# payload_number=(200 600 1500 2100 4600 6600) ; #spring
# payload_number=(10000 60000 860000 1910000 9710000 19560000) ; #php 
# payload_number=(10000 160000 710000 1410000 7260000 14860000) ; #golang

#for RSA Heroku

# payload_number=(60000 500000 3070000 4340000 9490000 10000000) ; #nodejs
# payload_number=(10000 40000 270000 610000 2470000 5800000) ; #django
# payload_number=(50000 70000 270000 560000 2710000 5560000) ; #spring
# payload_number=(10000 120000 410000 890000 4190000 9010000) ; #php
# payload_number=(10000 50000 190000 460000 2060000 4990000) ; #golang

# payload_number=(4340000) ; #nodejs
# payload_number=(610000) ; #django
# payload_number=(560000) ; #spring
# payload_number=(890000) ; #php
# payload_number=(460000) ; #golang

# spring  =>  [50000, 70000, 140000, 180000, 160000, 270000, 560000, 2710000, 5560000]
# php  =>  [10000, 120000, 170000, 240000, 340000, 410000, 890000, 4190000, 9010000]
# django  =>  [10000, 40000, 90000, 180000, 230000, 270000, 610000, 2470000, 5800000]
# golang  =>  [10000, 50000, 100000, 80000, 180000, 190000, 490000, 2620000, 4740000]
# nodejs  =>  [60000, 500000, 1170000, 1500000, 1830000, 3070000, 4340000, 9490000, 10000000]




# payload_number=(16001 23001) ; #nodejs



# connection_number=(10 25 50 100 200 400);
# concurrency_number=(2 4 6 8 10 12);

connection_number=(10 25 50);
concurrency_number=(2 4 6);

# framework_name="nodejs";
# framework_name="django";
# framework_name="spring";
# framework_name="golang";
# framework_name="php";

# framework_names=("nodejs" "golang" "spring" "django" "php");
framework_names=("nodejs");

for i in {1..10}; do
    for framework_name in ${framework_names[@]}; do

        curl "https://${framework_name}-cispa.herokuapp.com/";

        if [ "$framework_name" = "nodejs" ]; then
            payload_number=(60000 500000 3070000 4340000 9490000 10000000) ; #nodejs
        fi

        if [ "$framework_name" = "golang" ]; then
            payload_number=(10000 50000 190000 460000 2060000 4990000) ; #golang  
        fi

        if [ "$framework_name" = "spring" ]; then
            payload_number=(50000 70000 270000 560000 2710000 5560000) ; #spring
        fi

        if [ "$framework_name" = "django" ]; then
            payload_number=(10000 40000 270000 610000 2470000 5800000) ; #django
        fi

        if [ "$framework_name" = "php" ]; then
            payload_number=(10000 120000 410000 890000 4190000 9010000) ; #php
        fi

        # if [ "$framework_name" = "nodejs" ]; then
        #     payload_number=(9490000 10000000) ; #nodejs
        # fi

        # if [ "$framework_name" = "golang" ]; then
        #     payload_number=(2060000 4990000) ; #golang  
        # fi

        # if [ "$framework_name" = "spring" ]; then
        #     payload_number=(2710000 5560000) ; #spring
        # fi

        # if [ "$framework_name" = "django" ]; then
        #     payload_number=(2470000 5800000) ; #django
        # fi

        # if [ "$framework_name" = "php" ]; then
        #     payload_number=(4190000 9010000) ; #php
        # fi

        # if [ "$framework_name" = "nodejs" ]; then
        #     payload_number=(0 60000 240000 500000 1170000 1500000 1830000 3070000) ; #nodejs
        # fi

        # if [ "$framework_name" = "golang" ]; then
        #     payload_number=(0 10000 20000 50000 100000 80000 180000 190000) ; #golang  
        # fi

        # if [ "$framework_name" = "spring" ]; then
        #     payload_number=(0 50000 50000 70000 140000 180000 160000 270000) ; #spring
        # fi

        # if [ "$framework_name" = "django" ]; then
        #     payload_number=(0 10000 20000 40000 90000 180000 230000 270000) ; #django
        # fi

        # if [ "$framework_name" = "php" ]; then
        #     payload_number=(0 10000 30000 120000 170000 240000 340000 410000) ; #php
        # fi
        
        for t in ${payload_number[@]}; do
            # request_number=(10 15 20 25 30 35 40 45 50) ;
            request_number=(100 200 400 500 1000) ;
            # request_number=(100) ;
            for r in ${request_number[@]}; do
                ./wrk -t1 -c50 -d60s -R$r "https://${framework_name}-cispa.herokuapp.com/" 1 50 $framework_name $t 0 $i $r &
                sleep 10;
                if [ $t = 0 ]; then
                    ./wrk -t1 -c50 -d5s -R2000 "https://${framework_name}-cispa.herokuapp.com/?id=${t}" 1 50 $framework_name $t 1 $i $r >> "heroku/${framework_name}_${t}.txt" &
                else
                    ./wrk -t1 -c50 -d5s -R$r "https://${framework_name}-cispa.herokuapp.com/?id=${t}" 1 50 $framework_name $t 1 $i $r >> "heroku/${framework_name}_${t}_${r}.txt" &
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