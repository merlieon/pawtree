import './PedigreeBox.css'
import type { PedigreeNode } from '../types'

interface Props {
  node: PedigreeNode
}

function PedigreeBox({ node }: Props) {
  const hasChildren = node.mother || node.father

  return (
    <div className="pedigree-node">
      <div className="pedigree-box">
        <div className="pedigree-box__name">{node.individual.name}</div>
        <div className="pedigree-box__reg">{node.individual.reg_nr}</div>
      </div>

      {hasChildren && (
        <>
          <div className="pedigree-stub" />
          <div className="pedigree-children">
            {node.mother && <PedigreeBox node={node.mother} />}
            {node.father && <PedigreeBox node={node.father} />}
          </div>
        </>
      )}
    </div>
  )
}

export default PedigreeBox