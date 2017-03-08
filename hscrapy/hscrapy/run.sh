#!/bin/sh

check_hour() {
	HOUR=$(date +'%H')
	hours="08 09 10 11 12 13 14 15 16 17 18"
	for hour in $hours; do
		if [ $hour = $HOUR ]; then
			echo "True"
			return
		fi
	done

	echo "False"
}

CUR_DIR=$(pwd)

if [ $(check_hour) = "False" ]; then
	echo "not time to sync" >> /root/spider.log
	date >> /root/spider.log
	exit 0
fi

git pull &&

scrapy crawl octlink &&

cd dist &&
python ./octlink_deploy.py  &&

exit 0

tar -zcf $CUR_DIR/dist.tgz * &&
rm -rf /var/www/* &&
rm -rf /var/www/.idea &&
tar -zxf $CUR_DIR/dist.tgz -C /var/www &&
chmod 775 /var/www -R &&

date >> /root/spider.log
echo "run spider ocltink OK" >> /root/spider.log

exit 0
