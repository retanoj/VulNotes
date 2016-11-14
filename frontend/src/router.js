export function configRouter(router) {
    router.map({
        '/index': {
            name: 'main',
            title: '主页',
            auth: true,
            component: require('./components/VulNotes.vue')
        },
        '/login': {
            name: 'login',
            title: '登录',
            guest: true,
            component: require('./components/Login.vue')
        }
    })

    router.alias({
        '/': '/index'
    })

    router.beforeEach(function (transition){
        var token = localStorage.getItem('token')
        if (transition.to.auth){
            if (!token || token === null){
                transition.redirect('/login')
            }
        }

        if (transition.to.guest){
            if (token){
                transition.redirect('/')
            }
        }
        transition.next()
    })
}

