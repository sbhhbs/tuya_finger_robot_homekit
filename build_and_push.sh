docker buildx build \
  --platform linux/amd64 \
  --push -t sbhhbs/tuya_finger_robot_homekit:`git rev-parse --short HEAD` -t sbhhbs/tuya_finger_robot_homekit:latest .


