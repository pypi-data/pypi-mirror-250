<script lang="ts">
	import ParamViewer from "./ParamViewer.svelte";
	import type { Gradio } from "@gradio/utils";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import type { SelectData } from "@gradio/utils";

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: Record<
		string,
		{
			type: string;
			description: string;
			default: string;
		}
	>;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let gradio: Gradio<{
		change: never;
		select: SelectData;
		input: never;
	}>;
	export let linkify: string[] = [];

	// $: console.log({ value, linkify });
</script>

<!-- <Block {visible} {elem_id} {elem_classes} container={false} {scale} {min_width}> -->
{#if loading_status}
	<StatusTracker
		autoscroll={gradio.autoscroll}
		i18n={gradio.i18n}
		{...loading_status}
	/>
{/if}

<ParamViewer docs={value} {linkify} />
<!-- </Block> -->
