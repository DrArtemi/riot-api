<script>
    import SearchItem from "./SearchItem.svelte";

    export let name;
    export let data;
</script>

<h3 class="px-4 mt-4 mb-2 text-xl text-slate-400">{name}</h3>
<ul>
    {#each data as el (el.id)}
        <SearchItem name={el.name} link="/?category={name.toLowerCase()}&slug={el.slug}"/>
    {/each}
</ul>
