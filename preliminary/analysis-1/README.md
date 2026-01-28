```mermaid
---
title: IP Masking Through Misconfigured Reverse Proxy
---
sequenceDiagram
    autonumber

    participant Ext as External Client<br/>203.0.113.50
    participant Host as Host Machine<br/>46.62.168.233:80
    participant Nginx as nginx container<br/>172.18.0.3:80
    participant App as app container<br/>172.18.0.2:8080

    Note over Ext,App: Inbound Request Flow

    Ext->>Host: TCP SYN<br/>src: 203.0.113.50<br/>dst: 46.62.168.233:80

    Note over Host: Docker port mapping<br/>-p 80:80 → nginx

    Host->>Nginx: Forward to container<br/>src: 203.0.113.50<br/>dst: 172.18.0.3:80

    Note over Nginx: proxy_pass http://app:8080<br/>No X-Forwarded-For header set

    Nginx->>App: New TCP connection<br/>src: 172.18.0.3<br/>dst: 172.18.0.2:8080

    Note over App: Application sees:<br/>client_address = 172.18.0.3<br/>Real IP (203.0.113.50) is lost

    App-->>Nginx: HTTP 200 response
    Nginx-->>Host: Forward response
    Host-->>Ext: Response delivered

    Note over Ext,App: What Each Layer Knows

    Note over Host: Real client IP visible<br/>conntrack, tcpdump -i eth0

    Note over Nginx: Real client IP in $remote_addr<br/>Not forwarded to upstream

    Note over App: Only sees 172.18.0.3<br/>All visitors appear identical
```

## The Problem

nginx receives the real IP but doesn't pass it to the backend:

```nginx
location / {
    proxy_pass http://app:8080;
    # Missing: proxy_set_header X-Forwarded-For $remote_addr;
}
```

## Deploy

```bash
curl -fsSL https://raw.githubusercontent.com/Achxy/aurora-autopsy/main/preliminary/analysis-1/setup.sh | bash
```

## Verify

```bash
docker compose logs -f app
```

All visitors appear as `172.18.0.x` (nginx's container IP).\
![results](/assets/p-a1-1.png)
