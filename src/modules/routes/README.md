# Defined routes:

## Inplemented routes:

| Endpoint                         | Method                        | File                         |
| -------------------------------- | ----------------------------- | ---------------------------- |
| `/api/welcome/finish`            | `POST`                        | `routes_welcome.py`          |
| `/api/welcome/verifytotp`        | `POST`                        | `routes_welcome.py`          |
| `/api/welcome/totplink`          | `GET`                         | `routes_welcome.py`          |

| Endpoint                                    | Method                        | File                         |
| ------------------------------------------- | ----------------------------- | ---------------------------- |
| `/`                                         | `GET`                         | `routes.py`                  |
| `/api/auth`                                 | `POST`                        | `routes.py`                  |
| `/api/auth/validate`                        | `GET`                         | `routes.py`                  |

| Endpoint                                    | Method                        | File                         |
| ------------------------------------------- | ----------------------------- | ---------------------------- |
| `/api/dashboard/locale`                     | `GET` & `PATCH`               | `routes.py`                  |
| `/api/dashboard/locale/available`           | `GET`                         | `routes.py`                  | 
| `/api/dashboard/version`                    | `GET`                         | `routes.py`                  |
| `/api/dashboard/theme`                      | `GET`                         | `routes.py`                  |
| `/api/dashboard/update`                     | `GET`                         | `routes.py`                  |
| `/api/dashboard/configuration`              | `GET`                         | `routes.py`                  |
| `/api/dashboard/totpenabled`                | `GET`                         | `routes.py`                  |
| `/api/dashboard/statistics`                 | `GET`                         | `routes.py`                  |

| Endpoint                                    | Method                        | File                         |
| ------------------------------------------- | ----------------------------- | ---------------------------- |
| `/health` & `/healthz`                      | `GET`                         | `routes.py`                  |

| Endpoint                                    | Method                        | File                         |
| ------------------------------------------- | ----------------------------- | ---------------------------- |
| `/api/dashboard/wireguard/interfaces`       | `GET`                         | `routes.py`                  |

## Uninplemented routes:
