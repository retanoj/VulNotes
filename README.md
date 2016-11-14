# VulNotes 漏洞记录工具

## Requirements

Flask==0.11.1

Flask-Bootstrap==3.3.7.0

flask-marshmallow==0.7.0

Flask-Migrate==2.0.0

Flask-RESTful==0.3.5

Flask-Script==2.0.5

Flask-SQLAlchemy==2.1

gunicorn==19.6.0

PyJWT==1.4.2

mysql-connector==2.1.3

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

