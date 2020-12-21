<template>
    <div><p>Hello world</p></div>
</template>

<script>
import axios from 'axios'
export default {
    mounted(){
    var config = { headers: {account_id: this.$cookies.get('user-id'), session_id: this.$cookies.get('session-id')}}
    axios.get(this.$backend_url + "account/" + this.$cookies.get('user-id'), config).then(res => this.setDetails(res.data["account"]))
    },
    methods: {
        setDetails(data){
            console.log(data)
        }
    }
    
}

</script>