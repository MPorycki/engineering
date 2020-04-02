<template>
    <div class="container login-container" >
            <div class="row">
                <div class="col-md-6 login-form">
                    <h3>Rejestracja</h3>
                    <form @submit.prevent="register">
                        <div class="form-group">
                            <input type="text" id="email" class="form-control" placeholder="Podaj swój email" value="" />
                        </div>
                        <div class="form-group">
                            <input type="text" id="first_name" class="form-control" placeholder="Podaj swoje imię" value="" />
                        </div>
                        <div class="form-group">
                            <input type="text" id="last_name" class="form-control" placeholder="Podaj swoje nazwisko" value="" />
                        </div>
                        <div class="form-group">
                            <input type="password" id="password" class="form-control" placeholder="Wpisz hasło" value="" />
                        </div>
                        <div class="form-group">
                            <input type="password" id="password_confirm" class="form-control" placeholder="Potwierdź hasło" value="" />
                        </div>
                        <div class="form-group">
                            <input type="submit" class="btnSubmit" value="Zarejestruj się" />
                        </div>
                    </form>
                </div>
            </div>
        </div>
</template>

<script>
import axios from 'axios'
import backend_url from './variables'

export default {
    name: 'Registration',
    methods: {
    register(){
            var data = {
                email:document.getElementById("email").value,
                first_name: document.getElementById("first_name").value,
                last_name: document.getElementById("last_name").value,
                raw_password: document.getElementById("password").value,
                account_type: "customer"
            }
            if (this.validate_form()){
                axios.post(backend_url + "account/", data).then(res => this.register_success(res.data)).catch(error => this.handle_error(error.response.data));
            }
        },
        register_success(message){
            alert(message);
            this.$router.push({ name: 'Login', })
        },
        handle_error(error_data){
            if (error_data["email_taken"]) {
                this.add_error_text("email_error", "Podany mail jest zajety");
            }
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