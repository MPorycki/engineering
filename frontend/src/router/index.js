import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Registration from '../views/Registration.vue'
import PasswordResetVerification from '../views/PasswordResetVerification.vue'
import PasswordReset from '../views/PasswordReset.vue'
import VisitCreate from '../views/VisitCreate'
import AllVisits from '../views/AllVisits'
import AllSalons from '../views/AllSalons'
import VisitDetails from '../views/VisitDetails'
import VisitEdit from '../views/VisitEdit'
import AccountDetails from '../views/AccountDetails'
import AllCustomers from '../views/AllCustomers'
import AllServices from '../views/AllServices'
import ServiceDetails from '../views/ServiceDetails'
import VisitClose from '../views/VisitClose'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/registration',
    name: 'Registration',
    component: Registration
  },
  {
    path: '/passresetverify',
    name: 'PasswordResetVerification',
    component: PasswordResetVerification
  },
  {
    path: '/passreset',
    name: 'PasswordReset',
    component: PasswordReset
  }
  ,
  {
    path: '/visitCreate',
    name: 'VisitCreate',
    component: VisitCreate
  },
  {
    path: '/visitsAll',
    name: 'AllVisits',
    component: AllVisits
  },
  {
    path: '/visitDetails',
    name: 'VisitDetails',
    component: VisitDetails
  },
  {
    path: '/visitEdit',
    name: 'VisitEdit',
    component: VisitEdit
  }
  ,
  {
    path: '/allSalons',
    name: 'AllSalons',
    component: AllSalons
  },
  {
    path: '/accountDetails',
    name: 'AccountDetails',
    component: AccountDetails
  },
  {
    path: '/allCustomers',
    name: 'AllCustomers',
    component: AllCustomers
  },
  {
    path: '/allServices',
    name: 'AllServices',
    component: AllServices
  },
  {
    path: '/serviceDetails',
    name: 'ServiceDetails',
    component: ServiceDetails
  },
  {
    path: '/visitClose',
    name: 'VisitClose',
    component: VisitClose
  }
]

const router = new VueRouter({
  routes
})

export default router
