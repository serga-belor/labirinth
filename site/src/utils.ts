// Copyright Sergei Belorusets, 2024

export { AppendClassName };


function AppendClassName(to: string,
                         class_name: string
                        ): string
{
    if(to) {
        return to + " " + class_name;

    } else {
        return class_name;
    }
}
