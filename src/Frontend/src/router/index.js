import { createRouter, createWebHistory } from "vue-router";
import BrowsingRoles from "../components/views/staff/BrowseRolesListing.vue"
import CreateRoles from "../components/views/hr/RoleCreation.vue"
import RoleEditing from "../components/views/hr/RoleEditing.vue"
import IndivApplicant from "../components/views/hr/IndivApplicant.vue"
import IndivRoleListing from "../components/views/staff/IndivRoleListing.vue"
import LoginPage from "../components/views/LoginPage.vue"
import ViewAllApplicants from "../components/views/hr/ViewAllApplicants.vue"

const routes = [
    {
        path: '/',
        name: "Browsing Roles",
        component: BrowsingRoles
    },
    {
        path: '/RoleCreation',
        name: "Creation of Roles",
        component: CreateRoles
    },
    {
        path: '/IndivApplicant',
        name: "Individual Applicant",
        component: IndivApplicant
    },
    {
        path: '/ViewAllApplicants/:role_id',
        name: "View All Applicants",
        component: ViewAllApplicants
    },
    {
        path: '/IndivRoleListing/:role_id',
        name: "Individual Role Listing",
        component: IndivRoleListing
    },
    {
        path: '/Login',
        name: "Login",
        component: LoginPage
    },
    {
        path: '/RoleEditing/:role_id',
        name: "Role Editing",
        component: RoleEditing
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router