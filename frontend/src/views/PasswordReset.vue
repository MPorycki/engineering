<template>
    <div class="container login-container" >
            <div class="row">
                <div class="col-md-6 login-form">
                    <h3>Podaj nowe hasło</h3>
                    <form @submit.prevent="reset_password">
                         <div class="form-group">
                            <input type="password" id="password" class="form-control" placeholder="Wpisz hasło" value="" />
                            <b-tooltip target="password" id="password_error" class="rtooltips" triggers="hover" placement="right"  :disabled=true>{{password_text}}</b-tooltip>
                        </div>
                        <div class="form-group">
                            <input type="password" id="password_confirm" class="form-control" placeholder="Potwierdź hasło" value="" />
                        </div>
                        <div class="form-group">
                            <input type="submit" class="btnSubmit" value="Zresetuj hasło" />
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
        return {password_text: ""}
    },
    methods:{
        reset_password(){
            var data = {"new_password": document.getElementById("password").value, "reset_id": this.$route.query.reset_id}
            if (this.validate_password(data["new_password"], document.getElementById("password_confirm").value)){
                axios.patch(this.$backend_url+ "account/reset", data).then(() => this.reset_success()).catch(() => this.reset_fail())
            }
        },
        reset_success(){
            alert("Hasło zostało zmienione.")
            this.$router.push({ name: 'Login', })
            location.reload()
        },
        reset_fail(){
            alert("Zmiana hasłą nie powiodła się.")
        },
        validate_password(password, repeated_password){
             if ((password.replace(/\s/g, '')).length == 0){
                this.add_error("password", "Hasło jest wymagane")
                return false;
            } else if  ((password.replace(/\s/g, '')).length < 8) {
                this.add_error("password", "Minimalna ilość znaków to 8.")
                return false;
            } else if  ((password.replace(/\s/g, '')).length > 32) {
                this.add_error("password", "Maksymalna ilość znaków to 32.")
                return false;
            } else if (password != repeated_password){
                this.add_error("password", "Hasła nie zgadzają się")
                return false;
            } else {
                this.clear_error("password")
                return true;
            }
        },
        add_error(element_name, error_text){
            var form = document.getElementById(element_name);
            form.style.borderColor = "red"
            this.$root.$emit('bv::enable::tooltip', element_name + '_error')
            this.$root.$emit('bv::show::tooltip', element_name+ '_error')
            this.password_text = error_text
        },
        clear_error(element_name){
            var form = document.getElementById(element_name);
            form.style.borderColor = "#ced4da"
            this.$root.$emit('bv::disable::tooltip', element_name + '_error')
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
.FormLinks{
    color: #6998a3;
    font-weight: 600;
    text-decoration: none;
}
</style>