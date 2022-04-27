<script>
    import SearchItem from "./SearchItem.svelte";

    export let name;
    export let data;
</script>

<h3 class="px-4 mt-4 mb-2 text-xl text-slate-400">{name}</h3>
<ul>
    {#each data as el (el.id)}
        {#if name == "Players"}
            <SearchItem name={el.summoner_name} link="/{name.toLowerCase()}?name={el.summoner_name}&riot_id={el.riot_id}"/>
        {:else}
            <SearchItem name={el.name} link="/{name.toLowerCase()}?slug={el.slug}"/>
        {/if}
    {/each}
</ul>
