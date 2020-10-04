<template>
    <myForm>
        <h2>Moje wizyty</h2>
        <router-link to='/visitCreate' class="btnSubmit" >Umów wizytę </router-link>

           <table class="col text-center" id="myTable" v-for="visit in visits" :key="visit.visit_id">
                <router-link tag="tr" id="tblrow" class="btn btn-light shadow" :to="{ path: 'visitDetails', query: { id: visit.visit_id }}">
                    <td id="date">
                        {{visit.visit_date}}
                    </td>
                    <td >
                        {{visit.visit_data}}
                    </td>
                </router-link>
            </table>
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
            visits: []
        }
    },
    mounted(){
        axios.get(this.$backend_url + "accountVisits/ba0ea3715a514c52b2d8c6c917bec629").then(res => this.setVisits(res.data["visits"]))
    },
    methods: {
        setVisits(visitsInput){
            for (var i=0; i < visitsInput.length; i++) {
                this.visits.push(visitsInput[i])
            }
        }
    }
}
</script>

<style scoped>
    #myTable {
      margin-top: 25px;
    }

    #tblrow {
        height: 50px;
        width: 100%;
    }

    #date{
        padding-right: 100px;
        padding-left:25px;
        padding-top:10px;
    }
</style>