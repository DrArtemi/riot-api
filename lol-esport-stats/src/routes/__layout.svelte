<script>
    import { ApolloClient, InMemoryCache } from '@apollo/client/core';
    import { setClient } from "svelte-apollo";

    const client = new ApolloClient({
        uri: "http://localhost:3000/graphql",
        cache: new InMemoryCache()
    });
    setClient(client);
</script>

<slot></slot>