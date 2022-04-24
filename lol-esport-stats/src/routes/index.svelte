<script>
    import TopBar from '../components/TopBar.svelte'
    import Search from '../components/search/Search.svelte'
    import { ApolloClient, InMemoryCache } from '@apollo/client/core';
    import { setClient } from "svelte-apollo";

    const client = new ApolloClient({
		uri: "http://localhost:3000/graphql",
		cache: new InMemoryCache()
	});
    setClient(client);
</script>

<div class="search-bar">
    <Search />
</div>

<style>
    @import url('https://fonts.googleapis.com/css?family=Roboto&display=swap');
    :global(body) {
        font-family: 'Roboto', Arial, Helvetica, sans-serif;
    }

    .search-bar {
        margin-left: auto;
        margin-right: auto;
        width: 80%;
        padding: .5rem 2rem;
        border-radius: 5px;
        box-shadow: 0rem 0rem .25rem #b0bec5;
    }
</style>