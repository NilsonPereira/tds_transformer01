## launch script
SCMD="screen -dm -S transformer_app ./app.sh"
RESP=$(screen -ls)
SUB='transformer_app'
if [[ "$RESP" == *"$SUB"* ]]
then
  echo 'Process already exists'
else
  $SCMD
  echo 'Process created OK'
fi

