export interface Individual {
    reg_nr: string
    name: string
    chip_nr: string
    tattoo_id: string
    sex: 'male' | 'female'
    breed: string
    birth_date: Date
    mother_reg_nr: string | null
    father_reg_nr: string | null
}

export interface PedigreeNode {
    individual: Individual
    mother: PedigreeNode | null
    father: PedigreeNode | null
}