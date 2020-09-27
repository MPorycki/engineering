<template>
    <myForm>
        <h2>Moje wizyty</h2>
        <router-link to='/visitCreate' class="btnSubmit" >Umów wizytę </router-link>
    </myForm>
</template>


<script>
import myForm from '../components/myForm'

import axios from 'axios'
export default {
     components: {
        myForm
    },
    mounted(){
        axios.get(this.$backend_url + "accountVisits/ba0ea3715a514c52b2d8c6c917bec629").then(res => console.log(res.data))
    }
}
</script>