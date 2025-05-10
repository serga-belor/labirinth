// Copyright Sergei Belorusets, 2024-2025

export { AppendClassName };


function AppendClassName(to: string,
                         class_names: string[]
                        ): string
{
    return class_names.reduce(
        (result, class_name) => {
            if(result) {
                return  result + " " + class_name;

            } else {
                return class_name;
            }
        }, to);
}
