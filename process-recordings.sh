#!/bin/bash
echo "$(date +"%F %T") : Executing - process-recordings.py"
python /vox/rec-processor/process-recordings.py >> /vox/log/rec-processor.$(date +%F).log 2>&1
