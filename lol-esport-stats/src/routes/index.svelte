<script>
    import TopBar from '../components/TopBar.svelte'
    import Search from '../components/Search.svelte'
    import { ApolloClient, InMemoryCache } from '@apollo/client/core';
    import { setClient } from "svelte-apollo";

    const client = new ApolloClient({
		uri: "http://localhost:3000/graphql",
		cache: new InMemoryCache()
	});
    setClient(client);
</script>
<Search />
<TopBar />
<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
<p>coucou</p>

<style></style>