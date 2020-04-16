<template>
    <div class="container login-container" >
            <div class="row">
                <div class="col-md-6 login-form">
                    <h3>Podaj email Twojego konta</h3>
                    <h5>Na twoją skrzynkę wyślemy link umożliwiający reset hasła.</h5>
                    <form @submit.prevent="send_link">
                        <div class="form-group">
                            <input type="text" id="email" class="form-control" placeholder="Email" value="" />
                            <b-tooltip target="email" id="email_error" class="rtooltips" triggers="hover" placement="right"  :disabled=true >{{email_text}}</b-tooltip>
                        </div>
                        <div class="form-group">
                            <input type="submit" class="btnSubmit" value="Wyślij link" />
                        </div>
                    </form>
                </div>
            </div>
        </div>
</template>

<script>
import axios from 'axios'

export default {
    data(){
        return {email_text: ""}
    },
    methods:{
        send_link(){
            var data = {"email": document.getElementById("email").value}
            if (this.validate_email(data["email"])){
                axios.patch(this.$backend_url + 'account/reset_link', data).then(this.reset_link_sent()).catch(this.reset_link_sent_fail())
            }
        },
        validate_email(email){
             var email_regex = /.*@.*\.[a-z]{2,}/;
            if ((email.replace(/\s/g, '')).length > 32) {
                this.add_error("email", "Podany email jest za długi")
                return false;
            } else if ((email.replace(/\s/g, '')).length == 0){
                return false;
            } else if (!email_regex.test(email)){
                this.add_error("email", "Proszę wpisać email w poprawnym formacie")
                return false;
            } else {
                return true;
            }
        },
        add_error(element_name, error_text){
            var form = document.getElementById(element_name);
            form.style.borderColor = "red"
            this.$root.$emit('bv::enable::tooltip', element_name + '_error')
            this.$root.$emit('bv::show::tooltip', element_name+ '_error')
            switch(element_name){
                case "email":
                    this.email_text = error_text
                    break
                }
        },
        clear_error(element_name){
            var form = document.getElementById(element_name);
            form.style.borderColor = "#ced4da"
            this.$root.$emit('bv::disable::tooltip', element_name + '_error')
        },
        reset_link_sent(){
            alert("Link został wysłany na podany mail.")
            this.$router.push({ name: 'Login', })
            location.reload()
        },
        reset_link_sent_fail(){
            alert("Wysłanie linku nie powiodło się.")
        }
    }
}
</script>

<style scoped>
  .login-container{
    margin-top: 5%;
    margin-bottom: 5%;
}
.login-form{
    padding: 5%;
    box-shadow: 0 5px 8px 0 rgba(0, 0, 0, 0.2), 0 9px 26px 0 rgba(0, 0, 0, 0.19);
    margin-left:25%;
}
.login-form-1 h3{
    text-align: center;
    color: #333;
}
.login-container form{
    padding: 10%;
}
.btnSubmit
{
    width: 50%;
    border-radius: 1rem;
    padding: 1.5%;
    border: none;
    cursor: pointer;
}
.btnSubmit{
    font-weight: 600;
    color: #6998a3;
    background-color: #a4e6f4;
}
.btnSubmit:hover{
    color: #fff;
    background-color: #f3bac3;
}
.FormLinks{
    color: #6998a3;
    font-weight: 600;
    text-decoration: none;
}
</style>