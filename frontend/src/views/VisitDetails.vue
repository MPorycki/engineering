<template>
    <myForm>
        <H2>Szczegóły wizyty</H2>
        <div v-for="data in details" :key="data.id">
            <p>{{data["field_name"]}}</p> <br>
            <p>{{data["field_value"]}}</p>
        </div>
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
            visit: []
        }
    },
    mounted() {
        axios.get(this.$backend_url + "visit/"+this.$route.query.id).then(res => this.renderDetails(res.data))
    },
    methods: {
        renderDetails(details){
            console.log(details)
        }
    }
}
</script>