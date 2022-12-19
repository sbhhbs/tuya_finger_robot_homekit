docker buildx build \
  --platform linux/arm/v7,linux/arm64,linux/amd64 \
  --push -t sbhhbs/tuya_finger_robot_homekit:`git rev-parse --short HEAD` -t sbhhbs/tuya_finger_robot_homekit:latest .


