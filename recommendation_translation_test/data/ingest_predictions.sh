#!/bin/bash

function run_command {
  echo "$1"
  mysql --defaults-file=./replica.my.cnf -h tools.labsdb s53132__trex_p -e "$1"
  #psql test -c "$1"
}

columns="aawiki,abwiki,acewiki,adywiki,afwiki,akwiki,alswiki,amwiki,angwiki,anwiki,arcwiki,arwiki,arzwiki,astwiki,aswiki,avwiki,aywiki,azbwiki,azwiki,barwiki,bawiki,bclwiki,bewiki,bgwiki,bhwiki,biwiki,bjnwiki,bmwiki,bnwiki,bowiki,bpywiki,brwiki,bswiki,bugwiki,bxrwiki,cawiki,cdowiki,cebwiki,cewiki,chowiki,chrwiki,chwiki,chywiki,ckbwiki,cowiki,crhwiki,crwiki,csbwiki,cswiki,cuwiki,cvwiki,cywiki,dawiki,dewiki,diqwiki,dsbwiki,dtywiki,dvwiki,dzwiki,eewiki,elwiki,emlwiki,enwiki,eowiki,eswiki,etwiki,euwiki,extwiki,fawiki,ffwiki,fiwiki,fjwiki,fowiki,frpwiki,frrwiki,frwiki,furwiki,fywiki,gagwiki,ganwiki,gawiki,gdwiki,glkwiki,glwiki,gnwiki,gomwiki,gotwiki,guwiki,gvwiki,hakwiki,hawiki,hawwiki,hewiki,hifwiki,hiwiki,howiki,hrwiki,hsbwiki,htwiki,huwiki,hywiki,hzwiki,iawiki,idwiki,iewiki,igwiki,iiwiki,ikwiki,ilowiki,iowiki,iswiki,itwiki,iuwiki,jamwiki,jawiki,jbowiki,jvwiki,kaawiki,kabwiki,kawiki,kbdwiki,kgwiki,kiwiki,kjwiki,kkwiki,klwiki,kmwiki,knwiki,koiwiki,kowiki,krcwiki,krwiki,kshwiki,kswiki,kuwiki,kvwiki,kwwiki,kywiki,ladwiki,lawiki,lbewiki,lbwiki,lezwiki,lgwiki,lijwiki,liwiki,lmowiki,lnwiki,lowiki,lrcwiki,ltgwiki,ltwiki,lvwiki,maiwiki,mdfwiki,mgwiki,mhrwiki,mhwiki,minwiki,miwiki,mkwiki,mlwiki,mnwiki,mowiki,mrjwiki,mrwiki,mswiki,mtwiki,muswiki,mwlwiki,myvwiki,mywiki,mznwiki,nahwiki,napwiki,nawiki,ndswiki,newiki,newwiki,ngwiki,nlwiki,nnwiki,novwiki,nowiki,nrmwiki,nsowiki,nvwiki,nywiki,ocwiki,olowiki,omwiki,orwiki,oswiki,pagwiki,pamwiki,papwiki,pawiki,pcdwiki,pdcwiki,pflwiki,pihwiki,piwiki,plwiki,pmswiki,pnbwiki,pntwiki,pswiki,ptwiki,quwiki,rmwiki,rmywiki,rnwiki,rowiki,ruewiki,ruwiki,rwwiki,sahwiki,sawiki,scnwiki,scowiki,scwiki,sdwiki,sewiki,sgwiki,shwiki,simplewiki,siwiki,skwiki,slwiki,smwiki,snwiki,sowiki,sqwiki,srnwiki,srwiki,sswiki,stqwiki,stwiki,suwiki,svwiki,swwiki,szlwiki,tawiki,tcywiki,tetwiki,tewiki,tgwiki,thwiki,tiwiki,tkwiki,tlwiki,tnwiki,towiki,tpiwiki,trwiki,tswiki,ttwiki,tumwiki,twwiki,tyvwiki,tywiki,udmwiki,ugwiki,ukwiki,urwiki,uzwiki,vecwiki,vepwiki,vewiki,viwiki,vlswiki,vowiki,warwiki,wawiki,wowiki,wuuwiki,xalwiki,xhwiki,xmfwiki,yiwiki,yowiki,zawiki,zeawiki,zhwiki,zuwiki"
#columns=$(head -n1 $1 | cut -d',' -f2-)

column_names=$(echo $columns | sed "s/,/ $data_type, /g")

run_command "drop table if exists predictions;"

# mysql
id_type="varchar(20)"
data_type="decimal(15,14) default null"

# postgres
# id_type="varchar"
# data_type="decimal"

run_command "create table predictions (id $id_type, $column_names $data_type);"

# mysql
mkfifo /tmp/all.dat
chmod 666 /tmp/all.dat
bunzip2 -k -c $(realpath $1) > /tmp/all.dat &
run_command "load data local infile '/tmp/all.dat' replace into table predictions fields terminated by ',' lines terminated by '\n' ignore 1 rows;"
rm /tmp/all.dat

# postgres
# bunzip2 -k -c $(realpath $1) | psql test -c "\copy predictions from STDIN header delimiter ',' csv;"

