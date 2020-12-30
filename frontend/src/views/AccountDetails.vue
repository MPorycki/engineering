<template>
    <myForm>
        <H2>Szczegóły konta</H2>
        <h5><strong>Imię</strong></h5>
        <p>{{details.firstName}}</p>
        <h5><strong>Nazwisko</strong></h5>
        <p>{{details.lastName}}</p>
        <h5><strong>Email</strong></h5>
        <p>{{details.email}}</p>
    </myForm>
</template>

<script>
import myForm from '../components/myForm'

import axios from 'axios'
export default {
    components: {
        myForm
    },
    data(){
        return {
            details: [],
            id: ""
        }
    },
    mounted(){
    var config = { headers: {account_id: this.$cookies.get('user-id'), session_id: this.$cookies.get('session-id')}}
    axios.get(this.$backend_url + "account/" + this.$route.query.id, config).then(res => this.setDetails(res.data))
    },
    methods: {
        setDetails(data){
            this.details = data
        }
    }
    
}

</script>