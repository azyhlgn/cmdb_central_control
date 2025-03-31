#!/bin/bash

# 生成类似 MegaCli -PDList -aAll 的输出（模拟逻辑）
echo "Adapter #0"  # 假设只有一个 RAID 适配器

# 遍历所有物理磁盘
DISKS=$(lsblk -d -o NAME,TYPE | awk '$2=="disk"{print "/dev/"$1}')

for DISK in $DISKS; do
  DEVICE=${DISK##*/}  # 提取设备名（如 sda）
  MODEL=$(sudo smartctl -i $DISK | awk -F ': ' '/Device Model/{print $2}')
  SERIAL=$(sudo smartctl -i $DISK | awk -F ': ' '/Serial Number/{print $2}')
  CAPACITY=$(sudo smartctl -i $DISK | awk -F ': ' '/User Capacity/{print $2}' | sed 's/ \[.*//')
  INTERFACE=$(cat /sys/block/$DEVICE/device/transport 2>/dev/null || echo "UNKNOWN")
  HEALTH=$(sudo smartctl -H $DISK | awk '/SMART overall-health/{print $6}')

  # 模拟 Enclosure Device ID 和 Slot Number（基于 SCSI 主机/通道/目标）
  HOST=$(readlink /sys/block/$DEVICE | awk -F '/' '{print $5}' | sed 's/host//')
  CHANNEL=$(readlink /sys/block/$DEVICE | awk -F '/' '{print $6}' | sed 's/channel//')
  TARGET=$(readlink /sys/block/$DEVICE | awk -F '/' '{print $7}' | sed 's/target//')
  ENCLOSURE_ID=$((HOST + 0))  # 转换为数字
  SLOT_NUMBER=$(( (CHANNEL * 100) + TARGET ))  # 模拟槽位编号（自定义逻辑）

  # 输出格式化（对齐字段与 MegaCli 相似）
  echo "Enclosure Device ID: $ENCLOSURE_ID"
  echo "Slot Number: $SLOT_NUMBER"
  echo "Drive's position: DiskGroup: N/A, Span: N/A, Arm: N/A"
  echo "Device Id: $TARGET"
  echo "WWN: $(sudo smartctl -i $DISK | awk -F ': ' '/LU WWN Device Id/{print $2}' | sed 's/ //g')"
  echo "Sequence Number: 0"
  echo "Media Type: $(if [[ $MODEL == *"SSD"* ]]; then echo "Solid State Device"; else echo "Hard Disk Device"; fi)"
  echo "RAW Size: $CAPACITY"
  echo "Firmware state: Online"
  echo "SAS Address(0): $(sudo smartctl -i $DISK | awk -F ': ' '/SAS Address/{print $2}' | head -n1)"
  echo "Inquiry Data: $MODEL $SERIAL"
  echo "Media Error Count: 0"
  echo "Other Error Count: 0"
  echo "Predictive Failure Count: 0"
  echo "Last Predictive Failure Event: None"
  echo "PD Type: SATA"
  echo "Drive Temperature : N/A"
  echo "Smart Status: $HEALTH"
  echo " "
done