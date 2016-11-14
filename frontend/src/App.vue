<template>
    <div>
        <router-view></router-view>
    </div>
</template>

<script>
import Store from './vuex/store'

export default {
    store: Store
}
</script>
