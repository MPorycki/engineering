<template>
    <div class="container login-container" >
            <div class="row">
                <div class="col-md-6 login-form">
                    <slot>
                        Nothing loaded.
                    </slot>
                </div>
            </div>
        </div>
</template>


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