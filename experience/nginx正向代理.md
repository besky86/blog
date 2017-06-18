nginx正向代理配置：
```
 location ~ \/someuri {
        access_log /var/log/nginx/uploads.log;
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 300;
        proxy_pass $scheme://proxy_location$uri;
        recursive_error_pages on;
    }

```
如上面代码所示,可以进行正向代理，但这样会有问题：如果在url里面加了请求参数，用`$scheme://proxy_location$uri`转发后是不带这下请求参数的，所以不能使用`$uri`这个变量，如需要继续携带请求参数，则需要使用`$request_uri`，即`proxy_pass $scheme://proxy_location$request_uri;`

