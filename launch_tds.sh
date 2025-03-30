## launch script
SCMD="screen -dm -S transformer_tds ./tds.sh"
RESP=$(screen -ls)
SUB='transformer_tds'
if [[ "$RESP" == *"$SUB"* ]]
then
  echo 'Process already exists'
else
  $SCMD
  echo 'Process created OK'
fi

