import React, { useState, useRef, useEffect } from 'react';
import { Send, ArrowLeft, Mic, Paperclip, Globe, Scale } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { Message } from '../types';
import { sendChatStream } from '../api/api';
import LogoImg from './logo.png';

interface ChatInterfaceProps {
  onBackToLanding: () => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ onBackToLanding }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState('English');
  const [userMessageCount, setUserMessageCount] = useState(0);
  const [showLimitModal, setShowLimitModal] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const languages = ["English", "Hindi", "Bengali", "Tamil", "Telugu", "Marathi", "Gujarati", "Kannada", "Malayalam", "Punjabi", "Odia", "Urdu"];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    if (userMessageCount >= 2) {
      setShowLimitModal(true);
      return;
    }

    const userMessage: Message = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);
    
    // Increment count
    setUserMessageCount(prev => prev + 1);

    try {
      await sendChatStream({
        prompt: userMessage.content,
        language,
        history: messages
      }, (chunk) => {
        setMessages(prev => {
          const newMessages = [...prev];
          const lastMessage = newMessages[newMessages.length - 1];
          
          if (lastMessage && lastMessage.role === 'assistant') {
            // Append to existing bot message
            const updatedMessage = { ...lastMessage, content: lastMessage.content + chunk };
            newMessages[newMessages.length - 1] = updatedMessage;
            return newMessages;
          } else {
            // Add new bot message
            return [...prev, { role: 'assistant', content: chunk }];
          }
        });
      });

    } catch (error) {
      console.error(error);
      const errorMessage: Message = { role: 'assistant', content: "I encountered an error while processing your request. Please try again later." };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEndChat = () => {
    setMessages([]);
    onBackToLanding();
  };

  return (
    <div className="flex flex-col h-screen bg-judicial-cream font-sans overflow-hidden">
      
      {/* Header */}
      <div className="bg-white border-b border-judicial-brown/10 px-4 py-3 flex items-center justify-between shadow-sm z-10">
        <div className="flex items-center gap-4">
          <button 
              onClick={onBackToLanding}
              className="p-2 text-judicial-brown/60 hover:text-judicial-gold transition-colors rounded-full hover:bg-judicial-cream"
          >
              <ArrowLeft size={20} />
          </button>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-judicial-brown rounded-full flex items-center justify-center overflow-hidden border border-judicial-gold">
              <img 
                src={LogoImg} 
                alt="SAHAB Logo" 
                className="w-full h-full object-cover scale-125" 
              />
            </div>
            <div>
              <h2 className="font-serif font-bold text-judicial-brown leading-none">SAHAB</h2>
              <span className="text-[10px] text-judicial-gold font-bold tracking-wider uppercase">AI Legal Assistant</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 bg-judicial-cream px-3 py-1.5 rounded-full border border-judicial-brown/5">
           <Globe size={14} className="text-judicial-brown/60" />
           <select 
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-transparent text-sm text-judicial-brown font-medium focus:outline-none cursor-pointer"
            >
              {languages.map(lang => (
                <option key={lang} value={lang}>{lang}</option>
              ))}
            </select>
        </div>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto relative flex flex-col scrollbar-hide p-4 md:p-6">
        
        {/* Welcome Screen */}
        {messages.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center text-center animate-fade-in opacity-0" style={{ animationFillMode: 'forwards', animationDuration: '0.5s' }}>
            <div className="w-20 h-20 bg-judicial-gold/10 rounded-full flex items-center justify-center mb-6 border border-judicial-gold/20">
               <Scale size={40} className="text-judicial-gold" />
            </div>
            <h2 className="text-3xl font-serif font-bold text-judicial-brown mb-3">Namaste! I am SAHAB.</h2>
            <p className="text-judicial-brown/70 max-w-md mb-8 leading-relaxed">
              I can assist you with the Indian Penal Code, legal definitions, and Department of Justice services.
            </p>
            
            <div className="grid gap-3 w-full max-w-md">
               {['What is Section 420 of IPC?', 'How do I file an RTI?', 'Explain "Bail" simply.'].map((q, i) => (
                 <button 
                   key={i}
                   onClick={() => setInput(q)} 
                   className="text-left px-4 py-3 bg-white border border-judicial-brown/10 rounded-xl text-judicial-brown/80 text-sm hover:border-judicial-gold/50 hover:text-judicial-gold transition-colors shadow-sm"
                 >
                   "{q}"
                 </button>
               ))}
            </div>
          </div>
        ) : (
          /* Chat Screen */
          <div className="space-y-6 max-w-6xl mx-auto w-full">
            {messages.map((msg, idx) => {
              const isUser = msg.role === 'user';
              const showEndButton = !isUser; 

              return (
                <div key={idx} className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
                  <div 
                    className={`max-w-[85%] md:max-w-[75%] rounded-2xl px-6 py-4 text-base leading-relaxed shadow-sm ${
                      isUser 
                        ? 'bg-judicial-beige-dark text-judicial-brown rounded-tr-sm border border-judicial-brown/5' 
                        : 'bg-white text-judicial-brown rounded-tl-sm border border-judicial-brown/10'
                    }`}
                  >
                    {isUser ? (
                      <p className="whitespace-pre-wrap font-medium">{msg.content}</p>
                    ) : (
                      <div className="prose prose-sm max-w-none text-judicial-brown prose-headings:font-serif prose-headings:text-judicial-brown prose-strong:text-judicial-gold">
                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                      </div>
                    )}
                  </div>
                  
                  {showEndButton && (
                    <button 
                      onClick={handleEndChat}
                      className="mt-2 text-xs font-bold text-judicial-brown/40 hover:text-judicial-gold uppercase tracking-widest px-1 transition-colors flex items-center gap-1"
                    >
                      End Session
                    </button>
                  )}
                </div>
              );
            })}
            
            {isLoading && messages[messages.length - 1]?.role !== 'assistant' && (
              <div className="flex flex-col items-start">
                <div className="bg-white rounded-2xl rounded-tl-sm px-6 py-4 border border-judicial-brown/10 shadow-sm flex items-center gap-2">
                   <div className="w-1.5 h-1.5 bg-judicial-gold rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                   <div className="w-1.5 h-1.5 bg-judicial-gold rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                   <div className="w-1.5 h-1.5 bg-judicial-gold rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Bar */}
      <div className="p-4 bg-white border-t border-judicial-brown/10">
        <div className="max-w-6xl mx-auto">
          <form onSubmit={handleSend} className="relative flex items-center gap-3 bg-judicial-cream rounded-full border border-judicial-brown/10 px-2 shadow-inner focus-within:border-judicial-gold/50 focus-within:ring-1 focus-within:ring-judicial-gold/20 transition-all">
            
            <div className="flex items-center pl-2 gap-1 text-judicial-brown/40">
               <button type="button" className="p-2 hover:text-judicial-gold transition-colors"><Mic size={18}/></button>
               <button type="button" className="p-2 hover:text-judicial-gold transition-colors"><Paperclip size={18}/></button>
            </div>

            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLoading || showLimitModal}
              placeholder={showLimitModal ? "Limit reached. Please contact owner." : "Ask about IPC sections, legal definitions..."}
              className="flex-1 bg-transparent text-judicial-brown py-3.5 focus:outline-none placeholder-judicial-brown/40 text-sm"
            />
            
            <button 
              type="submit" 
              disabled={isLoading || !input.trim() || showLimitModal}
              className="p-2 m-1 bg-judicial-gold text-white rounded-full hover:bg-[#A0802D] disabled:opacity-30 disabled:hover:bg-judicial-gold transition-colors shadow-md"
            >
              <Send size={18} />
            </button>
          </form>
          <p className="text-center text-[10px] text-judicial-brown/40 mt-3">
             SAHAB provides general information, not legal advice. Please refer to official legal documents for verified information.
          </p>
        </div>
      </div>

      {/* Limit Reached Modal */}
      {showLimitModal && (
        <div className="fixed inset-0 z-50 bg-judicial-brown/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-md bg-white rounded-2xl p-8 shadow-2xl border-t-4 border-judicial-gold text-center">
             <div className="w-12 h-12 bg-judicial-cream rounded-full flex items-center justify-center mx-auto mb-4 text-judicial-gold">
               <Scale size={24} />
             </div>
             <h2 className="text-2xl font-serif font-bold text-judicial-brown mb-4">Usage Limit Reached</h2>
             <p className="text-judicial-brown/70 text-sm mb-6 leading-relaxed">
               You have reached the limit of 2 free queries. To continue using SAHAB, please contact the owner.
             </p>
             
             <a 
               href="https://sahil-bhoite.github.io/Website/" 
               target="_blank" 
               rel="noopener noreferrer"
               className="inline-flex items-center justify-center w-full bg-judicial-gold hover:bg-[#A0802D] text-white font-bold py-3.5 rounded-lg transition-colors shadow-lg mb-4"
             >
               Contact Owner
             </a>
             
             <button 
               onClick={() => onBackToLanding()}
               className="text-xs text-judicial-brown/60 hover:text-judicial-gold underline"
             >
               Back to Home
             </button>
          </div>
        </div>
      )}

    </div>
  );
};

export default ChatInterface;
