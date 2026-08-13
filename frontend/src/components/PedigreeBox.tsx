import type { PedigreeNode } from '../types'

interface Props {
  node: PedigreeNode
}

function PedigreeBox({ node }: Props) {
  const hasChildren = node.mother || node.father

  return (
    <div style={{ display: 'flex', alignItems: 'center' }}>
      <div style={{ border: '1px solid white', padding: '10px', borderRadius: '8px' }}>
        <div>{node.individual.name}</div>
        <div style={{ fontSize: '12px', opacity: 0.6 }}>{node.individual.reg_nr}</div>
      </div>

      {hasChildren && (
        <>
          <div style={{ width: '20px', height: '1px', background: 'white' }} />
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '20px',
            borderLeft: '1px solid white',
            paddingLeft: '20px',
          }}>
            {node.mother && <PedigreeBox node={node.mother} />}
            {node.father && <PedigreeBox node={node.father} />}
          </div>
        </>
      )}
    </div>
  )
}

export default PedigreeBox