<template>
    <myForm>
        <H2>{{details.name}}</H2>
        <h5><strong>Opis</strong></h5>
        <p>{{details.description}}</p>
        <h5><strong>Cena</strong></h5>
        <p>{{details.price}} PLN</p>
        <h5><strong>Czas trwania</strong></h5>
        <p>{{details.service_duration}} min</p>
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
        return{
            details: []
        }
    },
    mounted(){
        axios.get(this.$backend_url + "service/" +this.$route.query.id).then(res => this.setDetails(res.data))
    },
    methods:{
        setDetails(data){
            this.details = data
        }
    }

}
</script>