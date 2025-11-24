import React, { Suspense, useRef, useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Scale, Briefcase, Shield, Users, Building2, ChevronRight, MessageSquare, Globe, HelpCircle } from 'lucide-react';
import { Canvas, useFrame } from '@react-three/fiber';
import { useGLTF, OrbitControls, Environment, ContactShadows, PerspectiveCamera } from '@react-three/drei';
import * as THREE from 'three';
import LogoImg from './logo.png';

interface LandingPageProps {
  onLaunchApp: () => void;
}

function Model(props: any) {
  const { scene } = useGLTF('/models/angel_of_justice.glb');
  const group = useRef<THREE.Group>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (group.current) {
      // Initial "Crazy" State: Big and close to camera
      group.current.scale.set(5, 5, 5);
      group.current.position.set(0, 2, 5);
      group.current.rotation.y = Math.PI * 2; // Start with a full spin
      setReady(true);
    }
  }, []);

  // Track continuous rotation separately to avoid clock catch-up issues
  const rotationRef = useRef(0);

  useFrame((state, delta) => {
    if (group.current && ready) {
      // 1. Fly-in Animation (Lerp to final state)
      group.current.scale.lerp(new THREE.Vector3(1.25, 1.25, 1.25), 0.04);
      group.current.position.lerp(new THREE.Vector3(0, -1.4, 0), 0.04);
      
      // 2. Cursor Tracking & Rotation Logic
      // Continuous rotation using delta (prevents spinning fast after tab inactivity)
      rotationRef.current -= delta * 0.2;
      
      const mouseRotationY = state.mouse.x * 0.5;
      const mouseRotationX = state.mouse.y * 0.1;

      const targetRotationY = rotationRef.current + mouseRotationY;

      // Smooth interpolation
      group.current.rotation.y = THREE.MathUtils.lerp(group.current.rotation.y, targetRotationY, 0.05);
      group.current.rotation.x = THREE.MathUtils.lerp(group.current.rotation.x, mouseRotationX, 0.05);
    }
  });

  return (
    <group ref={group} {...props}>
      <primitive object={scene} />
    </group>
  );
}

const LandingPage: React.FC<LandingPageProps> = ({ onLaunchApp }) => {
  return (
    <div className="min-h-screen flex flex-col">
      {/* 1. Navigation Bar */}
      <nav className="sticky top-0 z-50 bg-judicial-cream/90 backdrop-blur-md border-b border-judicial-brown/10 px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-3">
            {/* Custom Logo with circular crop to hide watermark */}
            <div className="w-12 h-12 bg-judicial-brown rounded-full flex items-center justify-center overflow-hidden border-2 border-judicial-gold">
              <img 
                src={LogoImg} 
                alt="SAHAB Logo" 
                className="w-full h-full object-cover scale-125" 
              />
            </div>
            <div>
              <h1 className="font-serif font-bold text-xl tracking-tight text-judicial-brown leading-none">SAHAB</h1>
              <span className="text-[10px] uppercase tracking-wider text-judicial-brown/60 font-medium">Dept of Justice</span>
            </div>
          </div>
          
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-judicial-brown/80">
            <a href="#" className="hover:text-judicial-gold transition-colors">Home</a>
            <a href="#services" className="hover:text-judicial-gold transition-colors">Services</a>
            <a href="#about" className="hover:text-judicial-gold transition-colors">About AI</a>
            <div className="flex items-center gap-1 hover:text-judicial-gold transition-colors cursor-pointer">
              <Globe size={14} />
              <span>Languages</span>
            </div>
            <a href="#help" className="hover:text-judicial-gold transition-colors">Help</a>
          </div>

          <button 
            onClick={onLaunchApp}
            className="bg-judicial-gold text-white px-6 py-2.5 rounded-md font-semibold text-sm hover:bg-[#A0802D] transition-colors shadow-sm"
          >
            GET STARTED
          </button>
        </div>
      </nav>

      {/* 2. Hero Section */}
      <section className="relative pt-20 pb-32 px-6 overflow-hidden">
        {/* Mobile Background Watermark */}
        <div className="absolute inset-0 flex items-center justify-center md:hidden pointer-events-none opacity-5 overflow-hidden">
           <Scale size={400} className="text-judicial-brown translate-x-1/4" />
        </div>

        <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-12 items-center relative z-10">
          
          {/* Left Column: Text */}
          <div className="space-y-8 z-10">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-judicial-gold/10 text-judicial-gold text-xs font-bold uppercase tracking-widest mb-6 border border-judicial-gold/20">
                <Scale size={12} />
                Official AI Legal Assistant
              </div>
              <h1 className="text-5xl md:text-7xl font-serif font-bold text-judicial-brown leading-[1.1] mb-6">
                SAHAB <br/>
                <span className="text-4xl md:text-5xl font-light italic text-judicial-brown/80">Your Smart Legal Assistant</span>
              </h1>
              <p className="text-lg text-judicial-brown/70 max-w-xl leading-relaxed border-l-4 border-judicial-gold pl-6">
                Provide legal guidance based on the Indian Penal Code (IPC) and Department of Justice services, powered by advanced RAG + Gemini AI technology.
              </p>
            </motion.div>

            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="flex flex-wrap gap-4"
            >
              <button 
                onClick={onLaunchApp}
                className="px-8 py-4 bg-judicial-gold text-white rounded-lg font-semibold text-lg hover:bg-[#A0802D] transition-all shadow-lg hover:shadow-xl flex items-center gap-2"
              >
                GET STARTED <ChevronRight size={20} />
              </button>
              <button className="px-8 py-4 border-2 border-judicial-brown text-judicial-brown rounded-lg font-semibold text-lg hover:bg-judicial-brown hover:text-white transition-all">
                EXPLORE SERVICES
              </button>
            </motion.div>
          </div>

          {/* Right Column: 3D Statue */}
          <motion.div 
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 1, delay: 0.2 }}
            className="relative h-[600px] hidden md:flex items-center justify-center"
          >
            {/* Decorative Circle Background */}
            <div className="absolute w-[500px] h-[500px] rounded-full border border-judicial-gold/20 animate-spin-slow" style={{ animationDuration: '60s' }} />
            <div className="absolute w-[400px] h-[400px] rounded-full border border-judicial-brown/5" />
            
            {/* 3D Canvas */}
            <div className="relative z-10 w-full h-full">
               <Canvas>
                  <Suspense fallback={null}>
                    <PerspectiveCamera makeDefault position={[0, 0, 5]} fov={40} />
                    <ambientLight intensity={0.8} />
                    <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={1.5} castShadow />
                    <Environment preset="city" />
                    
                    {/* Animated Model */}
                    <Model />
                    
                    <ContactShadows position={[0, -1.4, 0]} opacity={0.6} scale={10} blur={2} far={4} />
                    <OrbitControls enableZoom={false} enableRotate={false} /> 
                  </Suspense>
               </Canvas>
            </div>
          </motion.div>
        </div>
      </section>

      {/* 3. Services Overview Section */}
      <section id="services" className="py-24 bg-white px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-serif font-bold text-judicial-brown mb-4">Areas of Practice</h2>
            <div className="w-24 h-1 bg-judicial-gold mx-auto" />
          </div>

          <motion.div 
            initial="hidden"
            whileInView="show"
            viewport={{ once: true }}
            variants={{
              hidden: { opacity: 0 },
              show: {
                opacity: 1,
                transition: {
                  staggerChildren: 0.1
                }
              }
            }}
            className="grid md:grid-cols-2 lg:grid-cols-3 gap-8"
          >
            <ServiceCard 
              icon={<Briefcase size={32} />}
              title="Business Law"
              description="Guidance on corporate regulations, contracts, and commercial disputes under Indian law."
              onClick={onLaunchApp}
            />
            <ServiceCard 
              icon={<Shield size={32} />}
              title="Criminal Law"
              description="Information regarding IPC sections, offenses, penalties, and legal procedures."
              onClick={onLaunchApp}
            />
            <ServiceCard 
              icon={<Users size={32} />}
              title="Family Law"
              description="Assistance with marriage acts, succession, guardianship, and family dispute resolution."
              onClick={onLaunchApp}
            />
            <ServiceCard 
              icon={<Building2 size={32} />}
              title="DoJ Services"
              description="Access to eCourts, Tele-Law, Legal Aid, and other Department of Justice citizen services."
              onClick={onLaunchApp}
            />
             {/* Added empty/promo cards to fill grid or keep it 3 columns */}
             <motion.div variants={{ hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0 } }} className="md:col-span-2 bg-judicial-cream border border-judicial-brown/10 rounded-xl p-8 flex items-center justify-between relative overflow-hidden group">
                <div className="relative z-10">
                  <h3 className="text-2xl font-serif font-bold text-judicial-brown mb-2">Need Custom Legal Help?</h3>
                  <p className="text-judicial-brown/70 mb-6 max-w-md">SAHAB can guide you to the right resources and forms for your specific legal needs.</p>
                  <button onClick={onLaunchApp} className="text-judicial-gold font-bold hover:underline flex items-center gap-1">ASK SAHAB <ChevronRight size={16}/></button>
                </div>
                <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-judicial-brown/5 transform skew-x-12 group-hover:bg-judicial-brown/10 transition-colors" />
             </motion.div>
          </motion.div>
        </div>
      </section>

      {/* 4. Chatbot Preview Section */}
      <section id="about" className="py-24 bg-judicial-cream px-6">
        <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-16 items-center">
          <div>
            <h2 className="text-3xl md:text-4xl font-serif font-bold text-judicial-brown mb-6">
              Instant Legal Clarity, <br/> In Your Language.
            </h2>
            <p className="text-lg text-judicial-brown/70 mb-8 leading-relaxed">
              SAHAB bridges the gap between complex legal jargon and plain language. Ask questions in English, Hindi, Tamil, Telugu, and more.
            </p>
            <div className="space-y-4">
              <FeatureItem text="24/7 Automated Assistance" />
              <FeatureItem text="Multilingual Support (12+ Languages)" />
              <FeatureItem text="Verified IPC & DoJ Information" />
            </div>
          </div>

          {/* Chat Preview UI */}
          <div className="bg-white rounded-2xl shadow-2xl border border-judicial-brown/5 overflow-hidden relative">
            <div className="bg-judicial-brown p-4 flex items-center gap-3">
              <div className="w-3 h-3 rounded-full bg-red-500" />
              <div className="w-3 h-3 rounded-full bg-yellow-500" />
              <div className="w-3 h-3 rounded-full bg-green-500" />
              <div className="ml-auto text-judicial-gold text-xs font-bold">SAHAB AI</div>
            </div>
            <div className="p-6 space-y-4 bg-judicial-cream/50 h-80 flex flex-col">
              <div className="self-start bg-white border border-judicial-brown/10 rounded-2xl rounded-tl-sm p-4 max-w-[80%] shadow-sm">
                <p className="text-judicial-brown text-sm">Namaste! I am SAHAB. How can I assist you with Indian Law today?</p>
              </div>
              <div className="self-end bg-judicial-brown text-white rounded-2xl rounded-tr-sm p-4 max-w-[80%] shadow-sm">
                <p className="text-sm">What is Section 420 of IPC?</p>
              </div>
              <div className="self-start bg-white border border-judicial-brown/10 rounded-2xl rounded-tl-sm p-4 max-w-[90%] shadow-sm">
                <p className="text-judicial-brown text-sm">
                  <span className="font-bold text-judicial-gold">Section 420 of the Indian Penal Code</span> deals with Cheating and dishonestly inducing delivery of property.
                  <br/><br/>
                  It prescribes punishment for anyone who cheats and thereby dishonestly induces the person deceived to deliver any property...
                </p>
              </div>
            </div>
            <div className="p-4 border-t border-judicial-brown/10 bg-white">
              <div className="flex gap-3 items-center">
                <div className="flex-1 bg-judicial-cream rounded-full px-4 py-2 text-sm text-judicial-brown/50 border border-judicial-brown/10">
                  Ask in English, Hindi, Tamil...
                </div>
                <button className="w-8 h-8 bg-judicial-gold rounded-full flex items-center justify-center text-white">
                  <ChevronRight size={16} />
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Footer */}
      <footer className="bg-[#151413] text-white/40 py-12 px-6 border-t border-white/5">
        <div className="max-w-7xl mx-auto grid md:grid-cols-4 gap-12">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-2 text-judicial-gold mb-6">
              <Scale size={24} />
              <span className="font-serif font-bold text-xl tracking-tight">SAHAB</span>
            </div>
            <p className="max-w-xs text-sm leading-relaxed mb-6">
              An initiative to make legal knowledge accessible to every citizen of India. Empowering justice through technology.
            </p>
            <div className="text-xs">© 2025 Department of Justice, Govt of India.</div>
          </div>
          
          <div>
            <h4 className="text-white font-serif font-bold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="hover:text-judicial-gold transition-colors">Home</a></li>
              <li><a href="#" className="hover:text-judicial-gold transition-colors">Services</a></li>
              <li><a href="#" className="hover:text-judicial-gold transition-colors">About SAHAB</a></li>
              <li><a href="#" className="hover:text-judicial-gold transition-colors">Contact</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-white font-serif font-bold mb-4">Legal & Privacy</h4>
            <p className="text-sm text-white/60 leading-relaxed">
              SAHAB is an AI assistant for informational purposes only and does not constitute legal advice. 
              Chat sessions are private and data is not permanently stored.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

const ServiceCard = ({ icon, title, description, onClick }: { icon: React.ReactNode, title: string, description: string, onClick: () => void }) => (
  <motion.div 
    variants={{
      hidden: { opacity: 0, y: 20 },
      show: { opacity: 1, y: 0 }
    }}
    className="group p-8 rounded-xl border border-judicial-brown/10 bg-white hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
  >
    <div className="w-14 h-14 bg-judicial-cream rounded-lg flex items-center justify-center text-judicial-brown mb-6 group-hover:bg-judicial-gold group-hover:text-white transition-colors">
      {icon}
    </div>
    <h3 className="text-xl font-serif font-bold text-judicial-brown mb-3">{title}</h3>
    <p className="text-judicial-brown/70 text-sm leading-relaxed mb-6 min-h-[60px]">
      {description}
    </p>
    <button 
      onClick={onClick}
      className="text-judicial-gold font-bold text-sm tracking-wide border-b-2 border-transparent group-hover:border-judicial-gold transition-all"
    >
      ASK SAHAB
    </button>
  </motion.div>
);

const FeatureItem = ({ text }: { text: string }) => (
  <div className="flex items-center gap-3 text-judicial-brown/80">
    <div className="w-1.5 h-1.5 rounded-full bg-judicial-gold" />
    <span className="font-medium">{text}</span>
  </div>
);

export default LandingPage;
