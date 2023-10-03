import { createRouter, createWebHistory } from "vue-router";
import BrowsingRoles from "../components/views/staff/BrowseRolesListing.vue"
import CreateRoles from "../components/views/hr/RoleCreation.vue"
import HomePage from "../HomePage.vue"
import IndivApplicant from "../components/views/hr/IndivApplicant.vue"
import IndivRoleListing from "../components/views/staff/IndivRoleListing.vue"

const routes = [
    {
        path: '/',
        name: "Home Page",
        component: HomePage
    },
    {
        path: '/browseroles',
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
        path: '/IndivRoleListing',
        name: "Individual Role Listing",
        component: IndivRoleListing
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router