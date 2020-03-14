#!/bin/bash

. backup.config

function main() {
  BACKUP_DATE=$( date +%Y-%m-%d_At_%H:%M:%S)

  cd "${BACKUP_DIR}" || exit 1

  pg_dumpall -r > roles.dump

  pg_dump -Fc -f ${BACKUP_DIR}/"backup-$BACKUP_DATE.dump" messenger

  BACKUP_COUNTER=`find . -type f | grep "backup" | wc -l`

  if [ ${BACKUP_COUNTER} -gt ${MAX_BACKUPS} ]
  then

    NEED_TO_DELETE_COUNTER=$((${BACKUP_COUNTER}-${MAX_BACKUPS}))

    local files=$(ls -l | grep "backup" | sort | head -n ${NEED_TO_DELETE_COUNTER} | awk -F' ' '{print $9}')
     echo "$files" | xargs rm -f

  fi

}

main $@