<script>
import LocaleText from "@/components/text/localeText.vue";
import {fetchGet, fetchPost} from "@/utilities/fetch.js";
import {DashboardConfigurationStore} from "@/stores/DashboardConfigurationStore.js";

export default {
	name: "dashboardLanguage",
	components: {LocaleText},
	setup(){
		const store = DashboardConfigurationStore()
		return {store}
	},
	data(){
		return {
			languages: undefined	
		}
	},
	mounted() {
		fetchGet("/api/dashboard/locale/available", {}, (res) => {
			this.languages = res.data;
		})
	},
	methods: {
		changeLanguage(lang_id){
			fetch("/api/dashboard/locale", {
				method: "PATCH",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ lang_id: lang_id }),
			})
			.then(res => res.json())
			.then(res => {
				if (res.status){
					this.store.Configuration.server.wgdashboard_language = lang_id;
					this.store.Locale = res.data;
				} else {
					this.store.newMessage("Server", "WGDashboard failed to update the language", "danger")
				}
			});
		}
	},
	computed:{
		currentLanguage(){
			let lang = this.store.Configuration.server.wgdashboard_language;
			return this.languages.find(x => x.lang_id === lang)
		}
	}
}
</script>

<template>
	<div>
		<small class="text-muted d-block mb-1">
			<strong><LocaleText t="Language"></LocaleText></strong>
		</small>
		<div class="d-flex gap-2">
			<div class="dropdown w-100">
				<button class="btn bg-primary-subtle text-primary-emphasis dropdown-toggle w-100 rounded-3" 
				        :disabled="!this.languages"
				        type="button" data-bs-toggle="dropdown" aria-expanded="false">
					<LocaleText t="Loading..." v-if="!this.languages"></LocaleText>
					<span v-else>
						{{ currentLanguage?.lang_name_localized }}
					</span>
					
				</button>
				<ul class="dropdown-menu rounded-3 shadow" style="max-height: 500px; overflow-y: scroll">
					<li v-for="x in this.languages">
						<a class="dropdown-item d-flex align-items-center" role="button"
							@click="this.changeLanguage(x.lang_id)"
						>
							<p class="me-auto mb-0">
								{{ x.lang_name_localized }}
								<small class="d-block" style="font-size: 0.8rem">
									{{ x.lang_name }}
								</small>
							</p>
							<i class="bi bi-check text-primary fs-5"
							   v-if="currentLanguage?.lang_id === x.lang_id"></i>
						</a>
					</li>
				</ul>
			</div>
		</div>
	</div>
</template>

<style scoped>
.dropdown-menu{
	width: 100%;
}

</style>