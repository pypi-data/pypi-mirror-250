import { colors } from "@gradio/theme";

type HighlightValueType = [string, string | null];

export function name_to_rgba(
	name: string,
	a: number,
	ctx: CanvasRenderingContext2D | null
): string {
	if (!ctx) {
		var canvas = document.createElement("canvas");
		ctx = canvas.getContext("2d")!;
	}
	ctx.fillStyle = name;
	ctx.fillRect(0, 0, 1, 1);
	const [r, g, b] = ctx.getImageData(0, 0, 1, 1).data;
	ctx.clearRect(0, 0, 1, 1);
	return `rgba(${r}, ${g}, ${b}, ${255 / a})`;
}

export function correct_color_map(
	color_map: Record<string, string>,
	browser: any,
	ctx: CanvasRenderingContext2D | null
): Record<string, { primary: string; secondary: string }> {
	var _color_map: Record<string, { primary: string; secondary: string }> = {};
	for (const col in color_map) {
		const _c = color_map[col].trim();

		if (_c in colors) {
			_color_map[col] = colors[_c as keyof typeof colors];
		} else {
			_color_map[col] = {
				primary: browser
					? name_to_rgba(color_map[col], 1, ctx)
					: color_map[col],
				secondary: browser
					? name_to_rgba(color_map[col], 0.5, ctx)
					: color_map[col]
			};
		}
	}
	return _color_map;
}

export function merge_elements(
	value: HighlightValueType[],
	mergeMode: "empty" | "equal"
): HighlightValueType[] {
	let result: HighlightValueType[] = [];
	let tempStr: string | null = null;
	let tempVal: string | null = null;

	for (const [str, val] of value) {
		if (
			(mergeMode === "empty" && val === null) ||
			(mergeMode === "equal" && tempVal === val)
		) {
			tempStr = tempStr ? tempStr + str : str;
		} else {
			if (tempStr !== null) {
				result.push([tempStr, tempVal as string]);
			}
			tempStr = str;
			tempVal = val;
		}
	}

	if (tempStr !== null) {
		result.push([tempStr, tempVal as string]);
	}

	return result;
}