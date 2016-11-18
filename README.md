# VulNotes 漏洞记录工具

## Requirements

Flask==0.11.1

Vue==1.0.26

gunicorn==19.6.0

PyJWT==1.4.2


## Usage

### Frontend

``` bash
# 前端项目在"frontend/"目录
# 安装依赖
npm install

# 变更PublicPath
# 若部署URL为http://a.b.com/vulnotes/, 则将PublicPath设置为'/vulnotes/'
change config/index.js: build: assetsPublicPath field

# 测试环境 localhost:8080
npm run dev

# 生产环境, 生成文件在'./frontend/dist'
npm run build
```

### Backend

```bash
# 用gunicorn启动flask app
$ ./run.sh
```

