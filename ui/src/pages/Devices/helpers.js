import {
  DEVICE_STATUS_ACTIVE,
  DEVICE_STATUS_ACTIVE_TITLE,
  DEVICE_STATUS_INACTIVE,
  DEVICE_STATUS_INACTIVE_TITLE,
  DEVICE_STATUS_APPROVED,
  DEVICE_STATUS_APPROVED_TITLE,
  DEVICE_STATUS_UNAPPROVED,
  DEVICE_STATUS_UNAPPROVED_TITLE,
} from './consts';


export function getStatusTitle(name) {
  switch (name) {
    case DEVICE_STATUS_ACTIVE:
      return DEVICE_STATUS_ACTIVE_TITLE;
    case DEVICE_STATUS_INACTIVE:
      return DEVICE_STATUS_INACTIVE_TITLE;
    case DEVICE_STATUS_APPROVED:
      return DEVICE_STATUS_APPROVED_TITLE;
    case DEVICE_STATUS_UNAPPROVED:
      return DEVICE_STATUS_UNAPPROVED_TITLE;
  }
}

export const statusOptions = [
  { value: DEVICE_STATUS_ACTIVE, label: DEVICE_STATUS_ACTIVE_TITLE },
  { value: DEVICE_STATUS_INACTIVE, label: DEVICE_STATUS_INACTIVE_TITLE },
  { value: DEVICE_STATUS_APPROVED, label: DEVICE_STATUS_APPROVED_TITLE },
  { value: DEVICE_STATUS_UNAPPROVED, label: DEVICE_STATUS_UNAPPROVED_TITLE },
];
