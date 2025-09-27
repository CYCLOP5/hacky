import React, { Suspense, useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Stars } from '@react-three/drei'
import * as THREE from 'three'

function Earth() {
  const meshRef = useRef<THREE.Mesh>(null)
  const atmosphereRef = useRef<THREE.Mesh>(null)
  
  // Create Earth texture
  const earthTexture = useMemo(() => {
    const canvas = document.createElement('canvas')
    canvas.width = 1024
    canvas.height = 512
    const ctx = canvas.getContext('2d')!
    
    // Ocean base
    ctx.fillStyle = '#1e40af'
    ctx.fillRect(0, 0, 1024, 512)
    
    // Add landmasses with more realistic colors
    ctx.fillStyle = '#22c55e' // Green for land
    
    // Africa
    ctx.beginPath()
    ctx.ellipse(200, 280, 70, 140, 0.2, 0, Math.PI * 2)
    ctx.fill()
    
    // Europe
    ctx.beginPath()
    ctx.ellipse(180, 180, 40, 60, 0, 0, Math.PI * 2)
    ctx.fill()
    
    // Asia
    ctx.beginPath()
    ctx.ellipse(350, 200, 150, 90, 0, 0, Math.PI * 2)
    ctx.fill()
    
    // North America
    ctx.beginPath()
    ctx.ellipse(750, 180, 80, 100, 0, 0, Math.PI * 2)
    ctx.fill()
    
    // South America
    ctx.beginPath()
    ctx.ellipse(780, 320, 50, 120, 0, 0, Math.PI * 2)
    ctx.fill()
    
    // Australia
    ctx.beginPath()
    ctx.ellipse(450, 380, 60, 30, 0, 0, Math.PI * 2)
    ctx.fill()
    
    // Ice caps
    ctx.fillStyle = '#f0f9ff'
    ctx.beginPath()
    ctx.ellipse(512, 40, 200, 25, 0, 0, Math.PI * 2)
    ctx.fill()
    ctx.beginPath()
    ctx.ellipse(512, 472, 200, 25, 0, 0, Math.PI * 2)
    ctx.fill()
    
    return new THREE.CanvasTexture(canvas)
  }, [])
  
  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.002
    }
    if (atmosphereRef.current) {
      atmosphereRef.current.rotation.y += 0.001
    }
  })

  return (
    <group>
      {/* Main Earth */}
      <mesh ref={meshRef} position={[0, 0, 0]}>
        <sphereGeometry args={[3, 64, 64]} />
        <meshStandardMaterial 
          map={earthTexture}
          roughness={0.8}
          metalness={0.1}
        />
      </mesh>
      
      {/* Atmospheric glow */}
      <mesh ref={atmosphereRef} position={[0, 0, 0]}>
        <sphereGeometry args={[3.15, 32, 32]} />
        <meshBasicMaterial 
          color="#87ceeb" 
          transparent 
          opacity={0.15}
          side={THREE.BackSide}
        />
      </mesh>
    </group>
  )
}

// Orbital Line Component
function OrbitLine({ radius, inclination, color, opacity = 0.3 }: any) {
  const points = useMemo(() => {
    const pts = []
    const segments = 64
    for (let i = 0; i <= segments; i++) {
      const angle = (i / segments) * Math.PI * 2
      const x = Math.sin(angle) * radius
      const z = Math.cos(angle) * radius
      const y = Math.sin(angle * inclination) * (radius * 0.3)
      pts.push(new THREE.Vector3(x, y, z))
    }
    return pts
  }, [radius, inclination])

  const geometry = useMemo(() => {
    const geom = new THREE.BufferGeometry().setFromPoints(points)
    return geom
  }, [points])

  return (
    <primitive object={new THREE.Line(geometry, new THREE.LineBasicMaterial({ 
      color: color, 
      transparent: true, 
      opacity: opacity 
    }))} />
  )
}

// Polar Orbit Line Component (for weather satellites)
function PolarOrbitLine({ radius, color, opacity = 0.3 }: any) {
  const points = useMemo(() => {
    const pts = []
    const segments = 64
    for (let i = 0; i <= segments; i++) {
      const angle = (i / segments) * Math.PI * 2
      const x = Math.sin(angle) * radius * 0.3
      const y = Math.cos(angle) * radius
      const z = Math.sin(angle * 2) * radius * 0.2
      pts.push(new THREE.Vector3(x, y, z))
    }
    return pts
  }, [radius])

  const geometry = useMemo(() => {
    const geom = new THREE.BufferGeometry().setFromPoints(points)
    return geom
  }, [points])

  return (
    <primitive object={new THREE.Line(geometry, new THREE.LineBasicMaterial({ 
      color: color, 
      transparent: true, 
      opacity: opacity 
    }))} />
  )
}

// Communication Satellite (Large with big solar panels)
function CommunicationSatellite({ orbitRadius, speed, inclination, phase }: any) {
  const groupRef = useRef<THREE.Group>(null)
  
  useFrame(({ clock }) => {
    const t = clock.getElapsedTime() * speed + phase
    if (groupRef.current) {
      // Equatorial orbit
      groupRef.current.position.x = Math.sin(t) * orbitRadius
      groupRef.current.position.z = Math.cos(t) * orbitRadius
      groupRef.current.position.y = Math.sin(t * inclination) * (orbitRadius * 0.2)
      groupRef.current.rotation.y = t * 2
    }
  })

  return (
    <group ref={groupRef}>
      {/* Main body */}
      <mesh>
        <boxGeometry args={[0.5, 0.8, 0.4]} />
        <meshStandardMaterial color="#d0d0d0" metalness={0.8} roughness={0.2} />
      </mesh>
      
      {/* Large solar panels */}
      <mesh position={[-1.2, 0, 0]}>
        <boxGeometry args={[0.8, 1.6, 0.03]} />
        <meshStandardMaterial color="#1a237e" metalness={0.1} roughness={0.8} />
      </mesh>
      <mesh position={[1.2, 0, 0]}>
        <boxGeometry args={[0.8, 1.6, 0.03]} />
        <meshStandardMaterial color="#1a237e" metalness={0.1} roughness={0.8} />
      </mesh>
      
      {/* Large communication dish */}
      <mesh position={[0, 0.5, 0]} rotation={[Math.PI / 6, 0, 0]}>
        <coneGeometry args={[0.3, 0.15, 16]} />
        <meshStandardMaterial color="#ffffff" metalness={0.7} roughness={0.3} />
      </mesh>
      
      {/* Antenna array */}
      <mesh position={[0, -0.5, 0]}>
        <cylinderGeometry args={[0.02, 0.02, 0.6]} />
        <meshStandardMaterial color="#ffaa00" metalness={0.9} roughness={0.1} />
      </mesh>
    </group>
  )
}

// GPS Satellite (Medium size, cubic)
function GPSSatellite({ orbitRadius, speed, inclination, phase }: any) {
  const groupRef = useRef<THREE.Group>(null)
  
  useFrame(({ clock }) => {
    const t = clock.getElapsedTime() * speed + phase
    if (groupRef.current) {
      // Medium Earth orbit
      groupRef.current.position.x = Math.sin(t) * orbitRadius
      groupRef.current.position.z = Math.cos(t) * orbitRadius
      groupRef.current.position.y = Math.sin(t * inclination) * (orbitRadius * 0.3)
      groupRef.current.rotation.z = t
    }
  })

  return (
    <group ref={groupRef}>
      {/* Cubic main body */}
      <mesh>
        <boxGeometry args={[0.4, 0.4, 0.4]} />
        <meshStandardMaterial color="#silver" metalness={0.9} roughness={0.1} />
      </mesh>
      
      {/* Cross-shaped solar panels */}
      <mesh position={[0, 0.6, 0]}>
        <boxGeometry args={[0.05, 0.4, 1.2]} />
        <meshStandardMaterial color="#1a237e" metalness={0.1} roughness={0.8} />
      </mesh>
      <mesh position={[0, -0.6, 0]}>
        <boxGeometry args={[0.05, 0.4, 1.2]} />
        <meshStandardMaterial color="#1a237e" metalness={0.1} roughness={0.8} />
      </mesh>
      
      {/* GPS antennas */}
      <mesh position={[0, 0, 0.3]}>
        <cylinderGeometry args={[0.08, 0.08, 0.1]} />
        <meshStandardMaterial color="#333333" />
      </mesh>
      <mesh position={[0, 0, -0.3]}>
        <cylinderGeometry args={[0.08, 0.08, 0.1]} />
        <meshStandardMaterial color="#333333" />
      </mesh>
    </group>
  )
}

// Weather Satellite (Polar orbit, cylindrical)
function WeatherSatellite({ orbitRadius, speed, inclination, phase }: any) {
  const groupRef = useRef<THREE.Group>(null)
  
  useFrame(({ clock }) => {
    const t = clock.getElapsedTime() * speed + phase
    if (groupRef.current) {
      // Polar orbit (nearly vertical)
      const angle = t
      groupRef.current.position.x = Math.sin(angle) * orbitRadius * 0.3
      groupRef.current.position.y = Math.cos(angle) * orbitRadius
      groupRef.current.position.z = Math.sin(angle * 2) * orbitRadius * 0.2
      groupRef.current.rotation.x = angle
    }
  })

  return (
    <group ref={groupRef}>
      {/* Cylindrical body */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[0.25, 0.25, 0.8]} />
        <meshStandardMaterial color="#4a90e2" metalness={0.6} roughness={0.4} />
      </mesh>
      
      {/* Solar panel wings */}
      <mesh position={[-0.7, 0, 0]}>
        <boxGeometry args={[0.6, 0.05, 1.0]} />
        <meshStandardMaterial color="#1a237e" metalness={0.1} roughness={0.8} />
      </mesh>
      <mesh position={[0.7, 0, 0]}>
        <boxGeometry args={[0.6, 0.05, 1.0]} />
        <meshStandardMaterial color="#1a237e" metalness={0.1} roughness={0.8} />
      </mesh>
      
      {/* Sensor array */}
      <mesh position={[0, -0.5, 0]} rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[0.15, 0.15, 0.2]} />
        <meshStandardMaterial color="#ff4444" emissive="#220000" emissiveIntensity={0.2} />
      </mesh>
    </group>
  )
}

// Space Station (Large, complex structure)
function SpaceStation({ orbitRadius, speed, phase }: any) {
  const groupRef = useRef<THREE.Group>(null)
  
  useFrame(({ clock }) => {
    const t = clock.getElapsedTime() * speed + phase
    if (groupRef.current) {
      // Low Earth orbit
      groupRef.current.position.x = Math.sin(t) * orbitRadius
      groupRef.current.position.z = Math.cos(t) * orbitRadius
      groupRef.current.position.y = Math.sin(t * 3) * (orbitRadius * 0.1)
      groupRef.current.rotation.y = t * 0.5
    }
  })

  return (
    <group ref={groupRef}>
      {/* Central hub */}
      <mesh>
        <cylinderGeometry args={[0.3, 0.3, 0.6]} />
        <meshStandardMaterial color="#e0e0e0" metalness={0.7} roughness={0.3} />
      </mesh>
      
      {/* Connecting modules */}
      <mesh position={[0.8, 0, 0]}>
        <cylinderGeometry args={[0.2, 0.2, 0.4]} />
        <meshStandardMaterial color="#cccccc" metalness={0.7} roughness={0.3} />
      </mesh>
      <mesh position={[-0.8, 0, 0]}>
        <cylinderGeometry args={[0.2, 0.2, 0.4]} />
        <meshStandardMaterial color="#cccccc" metalness={0.7} roughness={0.3} />
      </mesh>
      
      {/* Massive solar arrays */}
      <mesh position={[0, 1.2, 0]}>
        <boxGeometry args={[0.08, 2.0, 0.08]} />
        <meshStandardMaterial color="#444444" />
      </mesh>
      <mesh position={[0, 1.2, 0]}>
        <boxGeometry args={[2.4, 0.08, 1.6]} />
        <meshStandardMaterial color="#1a237e" metalness={0.1} roughness={0.8} />
      </mesh>
    </group>
  )
}

export function HeroScene(){
  return (
    <div style={{
      position:'fixed', 
      inset:0, 
      zIndex:0, 
      pointerEvents:'none', 
      opacity:0.7,
      background: `
        radial-gradient(ellipse 70% 40% at 50% 30%, rgba(0, 100, 200, 0.12) 0%, transparent 60%),
        radial-gradient(ellipse 50% 70% at 80% 80%, rgba(50, 150, 255, 0.08) 0%, transparent 50%),
        linear-gradient(135deg, rgba(15, 25, 45, 0.95) 0%, rgba(25, 35, 55, 0.98) 100%)
      `
    }}>
      <Canvas camera={{ position: [10, 6, 18], fov: 55 }}>
        <ambientLight intensity={0.3} />
        <pointLight position={[20, 20, 20]} intensity={1.2} color="#ffffff" />
        <pointLight position={[-15, -15, -15]} intensity={0.4} color="#4080ff" />
        <directionalLight 
          position={[12, 12, 12]} 
          intensity={0.8} 
          color="#a0c0ff"
        />
        <spotLight
          position={[25, 25, 25]}
          angle={0.4}
          penumbra={0.3}
          intensity={0.6}
          color="#60a0ff"
        />
        
        <Suspense fallback={null}>
          <Stars 
            radius={400} 
            depth={100} 
            count={12000} 
            factor={8} 
            saturation={0.9}
            fade 
            speed={0.3} 
          />
          <Earth />
          
          {/* Orbital Lines */}
          <OrbitLine radius={8} inclination={0.1} color="#0ea5e9" opacity={0.2} />
          <OrbitLine radius={9} inclination={0.2} color="#0ea5e9" opacity={0.15} />
          <OrbitLine radius={12} inclination={0.8} color="#3b82f6" opacity={0.25} />
          <PolarOrbitLine radius={7.5} color="#06b6d4" opacity={0.2} />
          <PolarOrbitLine radius={8.5} color="#06b6d4" opacity={0.15} />
          <OrbitLine radius={5.5} inclination={0.05} color="#8b5cf6" opacity={0.3} />
          
          {/* Multiple satellites with different orbits */}
          <CommunicationSatellite orbitRadius={8} speed={0.3} inclination={0.1} phase={0} />
          <CommunicationSatellite orbitRadius={9} speed={0.25} inclination={0.2} phase={Math.PI} />
          
          <GPSSatellite orbitRadius={12} speed={0.15} inclination={0.8} phase={0} />
          <GPSSatellite orbitRadius={12} speed={0.15} inclination={0.8} phase={Math.PI / 3} />
          <GPSSatellite orbitRadius={12} speed={0.15} inclination={0.8} phase={2 * Math.PI / 3} />
          
          <WeatherSatellite orbitRadius={7.5} speed={0.5} inclination={0} phase={0} />
          <WeatherSatellite orbitRadius={8.5} speed={0.4} inclination={0} phase={Math.PI / 2} />
          
          <SpaceStation orbitRadius={5.5} speed={0.8} phase={0} />
        </Suspense>
        
        <OrbitControls 
          enableZoom={false} 
          enablePan={false} 
          enableRotate={true}
          autoRotate={true}
          autoRotateSpeed={0.15}
          maxPolarAngle={Math.PI * 0.8}
          minPolarAngle={Math.PI * 0.2}
          dampingFactor={0.05}
          enableDamping={true}
        />
      </Canvas>
    </div>
  )
}