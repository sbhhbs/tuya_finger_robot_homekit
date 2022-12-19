docker buildx build \
  --platform linux/arm/v7,linux/arm64,linux/amd64 \
  --push -t sbhhbs/tv_switcher:`git rev-parse --short HEAD` -t sbhhbs/tuya_finger_robot_homekit:latest .


